# Wire JobFacts Consumers — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development. Steps use `- [ ]` for tracking.

**Goal:** Make three services consume the new `Signal.facts` (`JobFacts`) fields (salary, skills, date_posted) — currently populated but read by nothing.

**Architecture:** `Signal.facts.skills` becomes the deterministic input for `not_capability` flagging (bypasses LLM guess). `Signal.facts.date_posted` + `salary_max` become the sort key for the initiative-inference prompt (LLM sees strongest signals first). `Signal.facts.salary_*` + `skills` land in `Source` for CRM writeback.

**Tech Stack:** Python 3.13, Pydantic v2, FastAPI, Anthropic SDK, pytest.

**Spec:** `docs/PRD-account-intelligence.md` (PRD v1).

## Global Constraints

- Every mapped `not_capability` claim must be grounded in a real skill token from `Signal.facts.skills`. Never fabricate the flag.
- Extend YAML `not_capabilities` entries with an optional `signals: [str]` list — case-insensitive substring match against `facts.skills` items.
- All new tests must run offline. Mock at client boundaries.
- YAGNI. No refactors outside the three task surfaces.
- No schema changes beyond additive optional fields.

---

## File Map

- Modify `app/capability_map.yaml` — add `signals: [str]` to `three_phase_control`, `punch_list`, `safety_ehs`, `submittals_rfis`, `cost_change_orders`. Skip capabilities where no clean tokens exist.
- Modify `app/services/capabilities.py` — new helper `detect_flags_from_skills(signals, cmap) -> list[str]`. `map_capabilities` returns unchanged; deterministic flags are collected separately and rolled by `brief.py`.
- Modify `app/services/research.py` — call the helper alongside `map_capabilities`, pass results to `brief.assemble_brief`.
- Modify `app/services/initiatives.py` — sort signals by (date_posted desc, salary_max desc) before formatting for LLM.
- Modify `app/schemas/research.py` — add `salary_range: str | None = None`, `skills: list[str] = []` to `Source`.
- Modify `app/services/brief.py` — populate new `Source` fields from `Signal.facts`; merge deterministic-flags argument into `flags` (deduped alongside `capability_unverified` rollup).
- Modify `tests/test_capabilities.py`, `tests/test_brief.py` — new coverage.

---

### Task A: Deterministic not_capability flagging by skill token match

**Files:**
- Modify: `app/capability_map.yaml`
- Modify: `app/services/capabilities.py`
- Modify: `app/services/research.py`
- Modify: `app/services/brief.py`
- Modify: `app/schemas/research.py` (only if brief.py needs a new arg shape — it does not)
- Modify: `tests/test_capabilities.py`

**Interfaces:**
- Consumes: `list[Signal]` with populated `Signal.facts.skills`.
- Produces:
  - YAML `not_capabilities[*].signals: list[str]` (optional).
  - `capabilities.detect_flags_from_skills(signals: list[Signal], cmap: CapabilityMap) -> list[str]` — returns unique `"capability_unverified: <id>"` strings.
  - `brief.assemble_brief(...)` gains a keyword-only arg `deterministic_flags: list[str] = []`; merges into `flags` with existing dedupe.

- [ ] **Step 1: Add `signals` tokens to `not_capabilities` in `app/capability_map.yaml`**

Add a `signals: [str]` list (case-insensitive substring match) under each of these entries. Preserve existing keys.

```yaml
  - id: three_phase_control
    name: USACE / NAVFAC Three-Phase Control workflow
    note: "No confirmed native module. Flag capability_unverified: three_phase_control."
    signals: ["three-phase control", "three phase control", "usace", "navfac", "dfow", "qcm certification"]
  - id: punch_list
    name: Punch list management
    note: Stays in customer's PM / Cx system by design.
    signals: ["punch list", "punchlist"]
  - id: safety_ehs
    name: Safety / EHS management
    note: Out of scope.
    signals: ["ehs", "safety audit", "environmental health and safety"]
  - id: submittals_rfis
    name: Submittals / RFIs / document control
    note: Not offered.
    signals: ["submittals", "rfis", "rfi tracking", "document control"]
  - id: cost_change_orders
    name: Cost / change-order management
    note: Not offered.
    signals: ["change order", "cost report", "buyout"]
```

- [ ] **Step 2: Failing test in `tests/test_capabilities.py`**

```python
def test_detect_flags_from_skills_matches_three_phase_control():
    from app.schemas.research import JobFacts, Signal
    from app.services.capabilities import detect_flags_from_skills, load_capability_map

    load_capability_map.cache_clear()
    cmap = load_capability_map()
    signals = [
        Signal(
            type="job_posting",
            url="https://x/y",
            text="body",
            facts=JobFacts(skills=["Three-Phase Control Process", "USACE Compliance"]),
        )
    ]
    flags = detect_flags_from_skills(signals, cmap)
    assert "capability_unverified: three_phase_control" in flags


def test_detect_flags_dedupes_across_signals():
    from app.schemas.research import JobFacts, Signal
    from app.services.capabilities import detect_flags_from_skills, load_capability_map

    load_capability_map.cache_clear()
    cmap = load_capability_map()
    sigs = [
        Signal(type="job_posting", url="a", text="", facts=JobFacts(skills=["USACE"])),
        Signal(type="job_posting", url="b", text="", facts=JobFacts(skills=["NAVFAC", "DFOW"])),
    ]
    flags = detect_flags_from_skills(sigs, cmap)
    assert flags.count("capability_unverified: three_phase_control") == 1


def test_detect_flags_ignores_signals_without_facts():
    from app.schemas.research import Signal
    from app.services.capabilities import detect_flags_from_skills, load_capability_map

    load_capability_map.cache_clear()
    cmap = load_capability_map()
    sigs = [Signal(type="news", url="a", text="Three-Phase Control mentioned in prose")]
    assert detect_flags_from_skills(sigs, cmap) == []
```

Run: `pytest tests/test_capabilities.py -v`
Expected: 3 failures (helper undefined, YAML not loaded with signals).

- [ ] **Step 3: Update `NotCapability` model + `detect_flags_from_skills` in `app/services/capabilities.py`**

```python
class NotCapability(BaseModel):
    id: str
    name: str
    note: str = ""
    signals: list[str] = []


def detect_flags_from_skills(signals, cmap):
    """Return deterministic 'capability_unverified: <id>' flags from Signal.facts.skills.

    Case-insensitive substring match. Deduped. Ignores signals without JobFacts.
    """
    hits: list[str] = []
    seen: set[str] = set()
    for s in signals:
        facts = getattr(s, "facts", None)
        if not facts or not facts.skills:
            continue
        skill_blob = " | ".join(facts.skills).lower()
        for nc in cmap.not_capabilities:
            for token in nc.signals:
                if token.lower() in skill_blob:
                    flag = f"capability_unverified: {nc.id}"
                    if flag not in seen:
                        seen.add(flag)
                        hits.append(flag)
                    break
    return hits
```

- [ ] **Step 4: Wire helper into orchestrator**

Modify `app/services/research.py`:

```python
from app.services import angle, brief, capabilities, gaps, initiatives, questions, signals


def run_research(company_id, req):
    sigs = signals.gather_signals(domain=req.domain, name=req.name)
    if not sigs:
        return brief.assemble_brief(
            signals=[], initiatives=[], mapped=[], gaps=[], questions=[], angle="",
            deterministic_flags=[],
        )

    inits = initiatives.infer_initiatives(sigs)
    mapped = capabilities.map_capabilities(inits)
    cmap = capabilities.load_capability_map()
    det_flags = capabilities.detect_flags_from_skills(sigs, cmap)
    gap_list = gaps.synthesize_gaps(mapped)
    q_list = questions.generate_questions(gap_list)
    angle_text = angle.pick_angle(gap_list)

    return brief.assemble_brief(
        signals=sigs, initiatives=inits, mapped=mapped, gaps=gap_list,
        questions=q_list, angle=angle_text, deterministic_flags=det_flags,
    )
```

- [ ] **Step 5: Update `brief.assemble_brief` signature and dedupe**

```python
def assemble_brief(
    signals,
    initiatives,
    mapped,
    gaps,
    questions,
    angle,
    *,
    deterministic_flags: list[str] | None = None,
) -> ResearchBrief:
    ...
    flags: list[str] = []
    seen: set[str] = set()
    for m in mapped:
        if m.unverified_capability:
            f = f"capability_unverified: {m.unverified_capability}"
            if f not in seen:
                seen.add(f)
                flags.append(f)
    for f in (deterministic_flags or []):
        if f not in seen:
            seen.add(f)
            flags.append(f)
    ...
```

- [ ] **Step 6: Run tests**

Run: `pytest -q`
Expected: 22/22 pass (19 previous + 3 new).

- [ ] **Step 7: Commit**

```bash
git add app/capability_map.yaml app/services/capabilities.py \
        app/services/research.py app/services/brief.py \
        tests/test_capabilities.py
git commit -m "feat(capabilities): deterministic not_capability flags from Signal.facts.skills"
```

---

### Task B: Order signals by recency + salary before initiative inference

**Files:**
- Modify: `app/services/initiatives.py`
- Modify: `tests/test_signals.py` OR create `tests/test_initiatives.py` (prefer new file)

**Interfaces:**
- Consumes: `Signal.facts.date_posted` (ISO string, may be `None`) and `Signal.facts.salary_max` (float, may be `None`).
- Produces: `infer_initiatives(signals)` unchanged externally; internal order to LLM is (date_posted desc, salary_max desc, then original index as tiebreaker).

- [ ] **Step 1: Failing test in `tests/test_initiatives.py`**

```python
from unittest.mock import patch

from app.schemas.research import JobFacts, Signal


def _sig(url, skills=None, date=None, salary_max=None):
    return Signal(
        type="job_posting", url=url, text=f"body-{url}",
        facts=JobFacts(
            skills=skills or [], date_posted=date, salary_max=salary_max,
        ),
    )


def test_infer_initiatives_orders_signals_recent_then_salary():
    captured = {}

    def fake_llm(system, user, **kw):
        captured["user"] = user
        return '{"initiatives": []}'

    old = _sig("https://a", date="2025-01-01", salary_max=100000)
    new_hi = _sig("https://b", date="2026-08-01", salary_max=200000)
    new_lo = _sig("https://c", date="2026-08-01", salary_max=80000)

    with patch("app.services.initiatives.call_llm", side_effect=fake_llm):
        from app.services import initiatives
        initiatives.infer_initiatives([old, new_hi, new_lo])

    body = captured["user"]
    # Most recent + highest salary should appear before older ones.
    assert body.index("https://b") < body.index("https://a")
    assert body.index("https://c") < body.index("https://a")
    # Same date, higher salary first.
    assert body.index("https://b") < body.index("https://c")


def test_infer_initiatives_stable_when_facts_missing():
    signals = [
        Signal(type="news", url="https://n1", text="x"),
        Signal(type="news", url="https://n2", text="y"),
    ]
    captured = {}

    def fake_llm(system, user, **kw):
        captured["user"] = user
        return '{"initiatives": []}'

    with patch("app.services.initiatives.call_llm", side_effect=fake_llm):
        from app.services import initiatives
        initiatives.infer_initiatives(signals)

    body = captured["user"]
    assert body.index("https://n1") < body.index("https://n2")
```

Run: `pytest tests/test_initiatives.py -v`
Expected: FAIL — no ordering logic exists.

- [ ] **Step 2: Add ordering helper in `initiatives.py`**

```python
def _rank(sig):
    facts = getattr(sig, "facts", None)
    date = (facts.date_posted if facts and facts.date_posted else "")
    salary = (facts.salary_max if facts and facts.salary_max else 0.0)
    return (date, salary)


def infer_initiatives(signals):
    if not signals:
        return []
    ordered = sorted(
        enumerate(signals),
        key=lambda p: (_rank(p[1]), -p[0]),  # rank desc, then original order asc
        reverse=True,
    )
    signals_ordered = [s for _, s in ordered]
    user = _format_signals(signals_ordered)
    ...
```

Note the tuple trick: we want rank DESC, then original index ASC. Simpler to sort by `(-orig_index,)` then reverse, but the plan implementer may choose Python's `key=` with two passes for clarity — either is fine as long as tests pass.

- [ ] **Step 3: Run tests**

Run: `pytest tests/test_initiatives.py -v && pytest -q`
Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add app/services/initiatives.py tests/test_initiatives.py
git commit -m "feat(initiatives): order signals by recency then salary before LLM inference"
```

---

### Task C: Expose salary_range + skills on Source

**Files:**
- Modify: `app/schemas/research.py`
- Modify: `app/services/brief.py`
- Modify: `tests/test_brief.py`

**Interfaces:**
- Adds optional fields on `Source`:
  - `salary_range: str | None = None` — pre-formatted `"120000-165000 USD/YEAR"` or `None`.
  - `skills: list[str] = []`.
- `assemble_brief` populates them only when `Signal.type == "job_posting"` and `Signal.facts` is present.

- [ ] **Step 1: Extend `Source` in `app/schemas/research.py`**

```python
class Source(BaseModel):
    type: str
    url: str
    summary: str
    salary_range: str | None = None
    skills: list[str] = []
```

- [ ] **Step 2: Failing test in `tests/test_brief.py`**

```python
def test_brief_source_carries_salary_and_skills_for_jobs():
    from app.schemas.research import JobFacts, Signal
    sigs = [
        Signal(
            type="job_posting", url="https://x/y", text="Title...\n\nbody",
            facts=JobFacts(
                salary_min=120000, salary_max=165000,
                salary_currency="USD", salary_unit="YEAR",
                skills=["Three-Phase Control", "USACE Compliance"],
            ),
        ),
        Signal(type="news", url="https://n1", text="news body"),
    ]
    b = assemble_brief(
        signals=sigs, initiatives=[_init("x")], mapped=[],
        gaps=[], questions=[], angle="",
    )
    job_src = next(s for s in b.sources if s.url == "https://x/y")
    assert job_src.salary_range == "120000-165000 USD/YEAR"
    assert job_src.skills == ["Three-Phase Control", "USACE Compliance"]

    news_src = next(s for s in b.sources if s.url == "https://n1")
    assert news_src.salary_range is None
    assert news_src.skills == []
```

Run: `pytest tests/test_brief.py -v`
Expected: FAIL — Source lacks fields; brief doesn't populate them.

- [ ] **Step 3: Populate in `brief.assemble_brief`**

Replace the current `sources = [...]` line with a helper:

```python
def _format_salary_range(facts) -> str | None:
    if not facts:
        return None
    lo, hi = facts.salary_min, facts.salary_max
    if lo is None and hi is None:
        return None
    cur = facts.salary_currency or ""
    unit = f"/{facts.salary_unit}" if facts.salary_unit else ""
    if lo is not None and hi is not None:
        return f"{int(lo)}-{int(hi)} {cur}{unit}".strip()
    val = lo if lo is not None else hi
    return f"{int(val)} {cur}{unit}".strip()


sources = []
for s in signals:
    sources.append(
        Source(
            type=s.type,
            url=s.url,
            summary=s.text[:200],
            salary_range=_format_salary_range(s.facts) if s.type == "job_posting" else None,
            skills=list(s.facts.skills) if (s.type == "job_posting" and s.facts) else [],
        )
    )
```

- [ ] **Step 4: Run tests**

Run: `pytest -q`
Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add app/schemas/research.py app/services/brief.py tests/test_brief.py
git commit -m "feat(brief): expose salary_range and skills on Source for CRM writeback"
```

---

## Self-Review

- **Spec coverage:**
  - PRD §12 "cited claims only" → Task A grounds `not_capability` flags in real skill tokens.
  - PRD §9 output data model includes `ai_sources` — Task C enriches sources.
  - PRD §8 highest-weight job signals → Task B orders them explicitly by recency + salary.
- **Placeholder scan:** none.
- **Type consistency:** `Signal.facts` is `JobFacts | None`; all consumers guard on `facts` presence and on `type == "job_posting"` where relevant.
- **Cross-task shared file:** `brief.py` touched by A and C. Task order enforced (A before C).
