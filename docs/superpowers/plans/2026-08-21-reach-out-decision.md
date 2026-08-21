# Reach-Out Decision Field — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development. Steps use `- [ ]` for tracking.

**Goal:** Add a `reach_out` decision + `reach_out_reason` to `ResearchBrief` so sales reps get a clear act/defer/disqualify verdict alongside the brief.

**Architecture:** New LLM-decided service `app/services/reach_out.py::decide_reach_out(...)` runs between angle pick (step 6) and brief assembly (step 7). Takes mapped initiatives, gaps, angle, and signals (for recency). Returns `(recommendation, reason)`. `ResearchBrief` gains two required fields. Deterministic fallback: `"skip"` when `status="failed"` or gaps are empty, so the field is always populated.

**Tech Stack:** Python 3.13, Pydantic v2, FastAPI, Anthropic SDK (`call_llm`, `parse_json`), pytest.

**Spec:** `docs/PRD-account-intelligence.md` (PRD v1) — particularly §9 output data model and §12 guardrails ("no fabricated prospect facts").

## Global Constraints

- Values allowed: `"yes"` | `"hold"` | `"skip"`. Enforced by `Literal`.
- `reach_out_reason` is one short sentence, grounded in gaps / signals / flags actually present. Never invent evidence.
- Deterministic pre-check runs BEFORE the LLM call:
  - `status == "failed"` → `("skip", "no signals gathered")`
  - no mapped gaps (all `mapped_capability is None`) → `("skip", "no ELAS capability mapped to any initiative")`
  Otherwise → LLM decides.
- LLM prompt sees ONLY: gaps (gap + capability + impact), angle, `capability_unverified` flags, and the newest `date_posted` across job signals. Nothing else.
- On LLM parse failure → `("hold", "reach-out decision unavailable")`. Never crash the pipeline.
- Response must be valid JSON: `{"recommendation": "...", "reason": "..."}`.
- All new tests offline. Mock at `call_llm`.
- YAGNI. Do not touch angle, gaps, questions, capabilities services.

---

## File Map

- Modify `app/schemas/research.py` — add `ReachOut` literal + two fields on `ResearchBrief`.
- Create `app/services/reach_out.py` — `decide_reach_out(...)` with deterministic pre-check + LLM path.
- Modify `app/services/research.py` — call `decide_reach_out` after `pick_angle`, pass results into `assemble_brief`.
- Modify `app/services/brief.py` — accept `reach_out` and `reach_out_reason` args; set on brief.
- Create `tests/test_reach_out.py` — unit tests for the decision helper.
- Modify `tests/test_brief.py` — assert new fields populate.

---

### Task 1: Schema + brief plumbing

**Files:**
- Modify: `app/schemas/research.py`
- Modify: `app/services/brief.py`
- Modify: `tests/test_brief.py`

**Interfaces:**
- Adds `ReachOut = Literal["yes", "hold", "skip"]`.
- `ResearchBrief` gains `reach_out: ReachOut` and `reach_out_reason: str` (both required).
- `assemble_brief(...)` gains two keyword-only args: `reach_out: ReachOut = "skip"` and `reach_out_reason: str = ""`. Defaulting to `"skip"` keeps the field safe when a caller forgets to compute it, but the orchestrator must always compute it.

- [ ] **Step 1: Failing test in `tests/test_brief.py`**

```python
def test_brief_carries_reach_out_fields():
    b = assemble_brief(
        signals=[], initiatives=[_init("x")], mapped=[], gaps=[],
        questions=[], angle="", reach_out="yes", reach_out_reason="strong fit",
    )
    assert b.reach_out == "yes"
    assert b.reach_out_reason == "strong fit"


def test_brief_reach_out_defaults_to_skip():
    b = assemble_brief(
        signals=[], initiatives=[], mapped=[], gaps=[], questions=[], angle="",
    )
    assert b.reach_out == "skip"
    assert b.reach_out_reason == ""
```

Run: `pytest tests/test_brief.py -v`
Expected: FAIL — schema and function lack the fields.

- [ ] **Step 2: Extend `ResearchBrief` in `app/schemas/research.py`**

Add near existing `BriefStatus`:

```python
ReachOut = Literal["yes", "hold", "skip"]
```

Update `ResearchBrief`:

```python
class ResearchBrief(BaseModel):
    status: BriefStatus
    current_state: str
    initiatives: list[Initiative]
    gaps: list[Gap]
    discovery_questions: list[DiscoveryQuestion]
    recommended_angle: str
    reach_out: ReachOut
    reach_out_reason: str
    sources: list[Source]
    flags: list[str]
```

Field order matters only for readability; keep `reach_out` + `reach_out_reason` right after `recommended_angle`.

- [ ] **Step 3: Extend `assemble_brief` in `app/services/brief.py`**

Add keyword-only args and pass them into the constructor:

```python
def assemble_brief(
    signals: list[Signal],
    initiatives: list[Initiative],
    mapped: list[MappedInitiative],
    gaps: list[Gap],
    questions: list[DiscoveryQuestion],
    angle: str,
    *,
    reach_out: ReachOut = "skip",
    reach_out_reason: str = "",
) -> ResearchBrief:
    ...
    return ResearchBrief(
        status=status,
        current_state=current_state,
        initiatives=initiatives,
        gaps=gaps,
        discovery_questions=questions,
        recommended_angle=angle,
        reach_out=reach_out,
        reach_out_reason=reach_out_reason,
        sources=sources,
        flags=flags,
    )
```

Add `ReachOut` to the import at the top of `brief.py`.

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_brief.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add app/schemas/research.py app/services/brief.py tests/test_brief.py
git commit -m "feat(brief): add reach_out + reach_out_reason fields to ResearchBrief"
```

---

### Task 2: Decision helper service

**Files:**
- Create: `app/services/reach_out.py`
- Create: `tests/test_reach_out.py`

**Interfaces:**
- Consumes: `signals: list[Signal]`, `mapped: list[MappedInitiative]`, `gaps: list[Gap]`, `angle: str`, `status: BriefStatus`.
- Produces: `decide_reach_out(status, signals, mapped, gaps, angle) -> tuple[ReachOut, str]`.

- [ ] **Step 1: Failing tests in `tests/test_reach_out.py`**

```python
from unittest.mock import patch

from app.schemas.research import Gap, Initiative, JobFacts, MappedInitiative, Signal


def _init(txt="i"):
    return Initiative(initiative=txt, evidence="e", source_url="https://x")


def _mapped(cap=None):
    return MappedInitiative(initiative=_init(), matched_capability=cap, match_reason="r")


def _gap(cap="One live view of every inspection"):
    return Gap(gap="g", mapped_capability=cap, impact_hypothesis="h", initiative_ref=0)


def test_reach_out_deterministic_skip_when_failed():
    from app.services.reach_out import decide_reach_out
    r, reason = decide_reach_out(
        status="failed", signals=[], mapped=[], gaps=[], angle="",
    )
    assert r == "skip"
    assert "no signals" in reason.lower()


def test_reach_out_deterministic_skip_when_no_mapped_gaps():
    from app.services.reach_out import decide_reach_out
    r, reason = decide_reach_out(
        status="enriched",
        signals=[Signal(type="news", url="a", text="b")],
        mapped=[_mapped(cap=None)],
        gaps=[],
        angle="",
    )
    assert r == "skip"
    assert "no elas capability" in reason.lower()


def test_reach_out_calls_llm_when_gaps_present():
    from app.services import reach_out as ro
    fake = '{"recommendation":"yes","reason":"strong gap fit"}'
    sig = Signal(
        type="job_posting", url="https://x", text="b",
        facts=JobFacts(date_posted="2026-08-01"),
    )
    with patch("app.services.reach_out.call_llm", return_value=fake) as m:
        r, reason = ro.decide_reach_out(
            status="enriched",
            signals=[sig],
            mapped=[_mapped(cap="One live view of every inspection")],
            gaps=[_gap()],
            angle="wedge",
        )
    assert r == "yes"
    assert reason == "strong gap fit"
    assert m.call_count == 1


def test_reach_out_falls_back_to_hold_on_bad_json():
    from app.services import reach_out as ro
    with patch("app.services.reach_out.call_llm", return_value="not json"):
        r, reason = ro.decide_reach_out(
            status="enriched", signals=[], mapped=[_mapped(cap="X")], gaps=[_gap()],
            angle="w",
        )
    assert r == "hold"
    assert "unavailable" in reason.lower()


def test_reach_out_normalizes_unknown_recommendation_to_hold():
    from app.services import reach_out as ro
    fake = '{"recommendation":"maybe","reason":"unclear"}'
    with patch("app.services.reach_out.call_llm", return_value=fake):
        r, _ = ro.decide_reach_out(
            status="enriched", signals=[], mapped=[_mapped(cap="X")], gaps=[_gap()],
            angle="w",
        )
    assert r == "hold"
```

Run: `pytest tests/test_reach_out.py -v`
Expected: FAIL — module does not exist.

- [ ] **Step 2: Implement `app/services/reach_out.py`**

```python
import json
from typing import Iterable

from app.clients.anthropic import call_llm, parse_json
from app.schemas.research import (
    BriefStatus, Gap, MappedInitiative, ReachOut, Signal,
)

REACH_OUT_PROMPT = """
You decide whether a sales rep should reach out to this account NOW.

Inputs you will receive:
- GAPS: mapped ELAS capabilities the prospect appears to lack (with impact).
- ANGLE: the recommended outreach wedge.
- UNVERIFIED_FLAGS: capabilities ELAS does NOT have that the prospect may need.
- NEWEST_JOB_DATE: ISO date of the most recent job posting signal (or empty).

Return JSON: {"recommendation": "yes"|"hold"|"skip", "reason": "<one short sentence>"}

Rules for the recommendation:
- "yes": at least one strong mapped gap with a specific impact, AND signals are recent
  (newest job within ~90 days), AND the angle is concrete. Reason should cite the gap
  or the fresh signal.
- "hold": mapped gaps exist but signals are stale, thin, or heavily flagged as
  unverified; the account may be worth re-researching in 30 days.
- "skip": no mapped gaps at all, or every strong signal is dominated by
  capability_unverified flags — reaching out now would misrepresent ELAS.

Ground the reason in what is actually in the inputs. Never invent facts.
""".strip()


def _newest_job_date(signals: Iterable[Signal]) -> str:
    best = ""
    for s in signals:
        if s.type != "job_posting":
            continue
        facts = getattr(s, "facts", None)
        d = (facts.date_posted or "") if facts else ""
        if d and d > best:
            best = d
    return best


def decide_reach_out(
    *,
    status: BriefStatus,
    signals: list[Signal],
    mapped: list[MappedInitiative],
    gaps: list[Gap],
    angle: str,
) -> tuple[ReachOut, str]:
    if status == "failed":
        return "skip", "No signals gathered."
    if not any(m.matched_capability for m in mapped):
        return "skip", "No ELAS capability mapped to any initiative."

    flags = sorted(
        {m.unverified_capability for m in mapped if m.unverified_capability}
    )
    newest = _newest_job_date(signals)

    user = (
        "GAPS:\n"
        + "\n".join(
            f"- {g.gap} | capability: {g.mapped_capability} | impact: {g.impact_hypothesis}"
            for g in gaps
        )
        + f"\n\nANGLE:\n{angle}\n\n"
        f"UNVERIFIED_FLAGS: {', '.join(flags) if flags else '(none)'}\n"
        f"NEWEST_JOB_DATE: {newest or '(none)'}\n"
    )

    raw = call_llm(system=REACH_OUT_PROMPT, user=user)
    try:
        data = parse_json(raw)
        rec = data.get("recommendation")
        reason = str(data.get("reason") or "").strip()
    except (json.JSONDecodeError, TypeError, ValueError):
        return "hold", "Reach-out decision unavailable (LLM parse failure)."

    if rec not in ("yes", "hold", "skip"):
        return "hold", reason or "Reach-out decision unavailable (unknown recommendation)."
    if not reason:
        reason = f"LLM returned '{rec}' without a reason."
    return rec, reason
```

- [ ] **Step 3: Run tests**

Run: `pytest tests/test_reach_out.py -v`
Expected: 5/5 PASS.

- [ ] **Step 4: Commit**

```bash
git add app/services/reach_out.py tests/test_reach_out.py
git commit -m "feat(reach_out): add decide_reach_out helper with deterministic pre-check + LLM path"
```

---

### Task 3: Wire into orchestrator

**Files:**
- Modify: `app/services/research.py`
- Modify: `tests/test_research.py`

**Interfaces:**
- `run_research()` calls `decide_reach_out(status, signals, mapped, gaps, angle)` after `pick_angle`, before `assemble_brief`. Passes `(reach_out, reach_out_reason)` into `assemble_brief` as kw-args.
- The failure branch (no signals) also populates the fields — `reach_out="skip"`, `reach_out_reason="No signals gathered."`

- [ ] **Step 1: Failing test in `tests/test_research.py`**

Extend the existing test file (autouse fixture already blocks network):

```python
def test_research_populates_reach_out_field_default_failed():
    r = client.post("/research/companies/test-1", json={})
    body = r.json()
    assert body["reach_out"] == "skip"
    assert "no signals" in body["reach_out_reason"].lower()
```

Run: `pytest tests/test_research.py -v`
Expected: FAIL — orchestrator does not populate the field.

- [ ] **Step 2: Update `app/services/research.py`**

```python
from app.services import angle, brief, capabilities, gaps, initiatives, questions, reach_out, signals


def run_research(company_id: str, req: ResearchRequest) -> ResearchBrief:
    sigs = signals.gather_signals(domain=req.domain, name=req.name)
    if not sigs:
        return brief.assemble_brief(
            signals=[], initiatives=[], mapped=[], gaps=[], questions=[], angle="",
            reach_out="skip", reach_out_reason="No signals gathered.",
        )

    inits = initiatives.infer_initiatives(sigs)
    mapped = capabilities.map_capabilities(inits)
    gap_list = gaps.synthesize_gaps(mapped)
    q_list = questions.generate_questions(gap_list)
    angle_text = angle.pick_angle(gap_list)

    status = "enriched" if inits else "failed"
    ro_rec, ro_reason = reach_out.decide_reach_out(
        status=status, signals=sigs, mapped=mapped, gaps=gap_list, angle=angle_text,
    )

    return brief.assemble_brief(
        signals=sigs, initiatives=inits, mapped=mapped, gaps=gap_list,
        questions=q_list, angle=angle_text,
        reach_out=ro_rec, reach_out_reason=ro_reason,
    )
```

Note: the `status` computation duplicates what `brief.assemble_brief` does internally. That is intentional — we do NOT want `assemble_brief` to expose it, and we need to feed the reach-out helper. Leave `brief`'s own computation untouched.

- [ ] **Step 3: Run full suite**

Run: `pytest -q`
Expected: all previous tests + the new one pass.

- [ ] **Step 4: Commit**

```bash
git add app/services/research.py tests/test_research.py
git commit -m "feat(research): call decide_reach_out and thread verdict into brief"
```

---

## Self-Review

- **Spec coverage:**
  - PRD §9 output data model — new fields fit the same "structured, discrete field" pattern (not free-text dump).
  - PRD §12 guardrails — prompt explicitly instructs LLM to never invent facts; deterministic pre-check disqualifies `status="failed"`; parse-fail defaults to `"hold"` not `"yes"`.
  - PRD §14 success metrics — `reach_out="yes"` becomes the funnel signal for "% enriched briefs where rep actually acted."
- **Placeholder scan:** none.
- **Type consistency:**
  - `ReachOut` literal used consistently in schema, service, and brief.
  - `decide_reach_out` signature uses keyword-only args; orchestrator matches.
  - `assemble_brief` gains kw-only args with defaults so the fail-branch call site is one line shorter.
- **Cross-task shared file:** `brief.py` in Task 1, `research.py` in Task 3 (independent). No parallel dispatch risk since we run sequentially.
