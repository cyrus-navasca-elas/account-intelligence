# Wire Apify Pipeline — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the account-intelligence pipeline produce a real `ResearchBrief` end-to-end using the `fantastic-jobs/career-site-job-listing-api` Apify actor as the signal source.

**Architecture:** Existing scaffold in `app/services/` is largely stub-implemented. This plan fixes the Apify client input/output contract, updates signal mapping, propagates capability-map flags into the brief, backfills unit tests, and runs a live smoke test.

**Tech Stack:** FastAPI, Pydantic v2, `apify-client`, Anthropic SDK, PyYAML, pytest.

**Spec:** `docs/PRD-account-intelligence.md` (PRD v1) + `docs/pipeline-steps.md` (build order).

## Global Constraints

- Python 3.13+. Pydantic v2. FastAPI.
- Actor id fixed: `fantastic-jobs/career-site-job-listing-api` (settings.apify_jobs_actor_id).
- Capability-map source of truth: `app/capability_map.yaml`. Never claim a match against `not_capabilities` — surface as `ai_flags` entry `capability_unverified: <id>`.
- Never invent prospect facts. If web yields nothing → `status="failed"`, empty arrays.
- All new tests must run offline (no network). Mock Apify + Anthropic at the client boundary.
- Job posting is the highest-weight signal (per PRD §8). Default cap: 25 jobs / 6-month window / company (to keep Apify cost bounded at ~$0.10/company).
- Never write to `.env` from code. Never log the API key.

---

## File Map

- Modify `app/clients/apify.py` — real actor input schema + typed output shape.
- Modify `app/services/signals.py` — map actor's `description_text`/`url`/`date_posted` fields.
- Modify `app/services/brief.py` — include `unverified_capability` in `flags`; drop noisy `unmatched_initiative` flag.
- Create `tests/test_apify_client.py` — client input assembly + output normalization (mocked).
- Create `tests/test_signals.py` — signal mapping.
- Create `tests/test_capabilities.py` — YAML load + mapping validation.
- Create `tests/test_brief.py` — flag rollup + status derivation.
- Create `scripts/smoke_apify.py` — one-shot live end-to-end run against a real domain (manual).

---

### Task 1: Fix Apify actor input contract

**Files:**
- Modify: `app/clients/apify.py`
- Create: `tests/test_apify_client.py`

**Interfaces:**
- Consumes: `settings.apify_api_key`, `settings.apify_jobs_actor_id`.
- Produces: `fetch_job_postings(domain: str, name: str | None = None, *, limit: int = 25, time_range: str = "6m") -> list[dict]` — returns raw dataset items from Apify, unchanged shape.

- [ ] **Step 1: Write failing test for input assembly**

```python
# tests/test_apify_client.py
from unittest.mock import MagicMock, patch

def test_fetch_job_postings_builds_correct_run_input():
    from app.clients import apify

    fake_actor = MagicMock()
    fake_actor.call.return_value = {"defaultDatasetId": "ds1"}
    fake_client = MagicMock()
    fake_client.actor.return_value = fake_actor
    fake_client.dataset.return_value.iterate_items.return_value = iter([])

    with patch("app.clients.apify.ApifyClient", return_value=fake_client), \
         patch.object(apify.settings, "apify_api_key", "k"), \
         patch.object(apify.settings, "apify_jobs_actor_id", "fantastic-jobs/career-site-job-listing-api"):
        apify.fetch_job_postings("prospect.com")

    fake_client.actor.assert_called_once_with("fantastic-jobs/career-site-job-listing-api")
    (kwargs,) = fake_actor.call.call_args_list
    ri = kwargs.kwargs["run_input"]
    assert ri["domainFilter"] == ["prospect.com"]
    assert ri["timeRange"] == "6m"
    assert ri["limit"] == 25
    assert ri["descriptionType"] == "text"
```

- [ ] **Step 2: Run test, verify failure**

Run: `pytest tests/test_apify_client.py::test_fetch_job_postings_builds_correct_run_input -v`
Expected: FAIL — current `run_input={"domain": ..., "companyName": ...}` doesn't match.

- [ ] **Step 3: Rewrite `fetch_job_postings`**

```python
# app/clients/apify.py
from app.config import settings


def fetch_job_postings(
    domain: str,
    name: str | None = None,
    *,
    limit: int = 25,
    time_range: str = "6m",
) -> list[dict]:
    """Fetch recent job postings for a company via the career-site actor.

    Returns raw dataset items exactly as the actor emits them.
    """
    if not settings.apify_api_key or not settings.apify_jobs_actor_id:
        return []

    from apify_client import ApifyClient

    client = ApifyClient(settings.apify_api_key)
    run_input: dict = {
        "domainFilter": [domain],
        "timeRange": time_range,
        "limit": limit,
        "descriptionType": "text",
    }
    run = client.actor(settings.apify_jobs_actor_id).call(run_input=run_input)
    if not run:
        return []
    return list(client.dataset(run["defaultDatasetId"]).iterate_items())
```

- [ ] **Step 4: Add failing test — returns [] when key missing**

```python
def test_fetch_job_postings_returns_empty_without_key():
    from app.clients import apify
    with patch.object(apify.settings, "apify_api_key", ""):
        assert apify.fetch_job_postings("prospect.com") == []
```

- [ ] **Step 5: Run full test file**

Run: `pytest tests/test_apify_client.py -v`
Expected: PASS both tests.

- [ ] **Step 6: Commit**

```bash
git add app/clients/apify.py tests/test_apify_client.py
git commit -m "fix(apify): use actor's real input schema (domainFilter/timeRange/limit)"
```

---

### Task 2: Map actor output → Signal

**Files:**
- Modify: `app/services/signals.py`
- Create: `tests/test_signals.py`

**Interfaces:**
- Consumes: `apify.fetch_job_postings()` returns dicts with keys: `url`, `title`, `description_text`, `date_posted`, `organization`, `locations_derived`.
- Produces: `gather_signals(domain, name) -> list[Signal]` where each job → `Signal(type="job_posting", url=job["url"], text="<title>\n\n<description_text>")`.

- [ ] **Step 1: Write failing test for job → Signal mapping**

```python
# tests/test_signals.py
from unittest.mock import patch

from app.schemas.research import Signal


def test_gather_signals_maps_jobs_to_signals():
    fake_jobs = [
        {
            "url": "https://boards.greenhouse.io/x/jobs/1",
            "title": "QC Manager - NAVFAC",
            "description_text": "Own Three-Phase Control across $20M+ jobs.",
            "date_posted": "2026-08-10",
        }
    ]
    with patch("app.services.signals.apify.fetch_job_postings", return_value=fake_jobs), \
         patch("app.services.signals.web_search.search_company_signals", return_value=[]):
        from app.services import signals
        out = signals.gather_signals(domain="prospect.com", name="Prospect")

    assert len(out) == 1
    s = out[0]
    assert isinstance(s, Signal)
    assert s.type == "job_posting"
    assert s.url == "https://boards.greenhouse.io/x/jobs/1"
    assert "QC Manager - NAVFAC" in s.text
    assert "Three-Phase Control" in s.text


def test_gather_signals_skips_jobs_without_description():
    fake_jobs = [{"url": "https://x/y", "title": "T", "description_text": ""}]
    with patch("app.services.signals.apify.fetch_job_postings", return_value=fake_jobs), \
         patch("app.services.signals.web_search.search_company_signals", return_value=[]):
        from app.services import signals
        out = signals.gather_signals(domain="prospect.com", name=None)
    assert out == []
```

- [ ] **Step 2: Run tests, verify failure**

Run: `pytest tests/test_signals.py -v`
Expected: FAIL — current code reads `j.get("description")` not `description_text`, and produces a signal even with empty text.

- [ ] **Step 3: Rewrite job-mapping block in `signals.py`**

Replace the `if domain:` job loop with:

```python
    if domain:
        jobs = apify.fetch_job_postings(domain, name)
        for j in jobs:
            desc = str(j.get("description_text") or "").strip()
            if not desc:
                continue
            title = str(j.get("title") or "").strip()
            url = str(j.get("url") or "")
            text = f"{title}\n\n{desc}" if title else desc
            signals.append(Signal(type="job_posting", url=url, text=text))
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_signals.py -v`
Expected: PASS both.

- [ ] **Step 5: Commit**

```bash
git add app/services/signals.py tests/test_signals.py
git commit -m "fix(signals): map actor's description_text and skip empty jobs"
```

---

### Task 3: Roll `unverified_capability` into brief.flags

**Files:**
- Modify: `app/services/brief.py`
- Create: `tests/test_brief.py`

**Interfaces:**
- Consumes: `MappedInitiative.unverified_capability: str | None`.
- Produces: `assemble_brief(...) -> ResearchBrief` — each `MappedInitiative` with `unverified_capability=X` contributes `f"capability_unverified: {X}"` to `brief.flags` (deduped). Drops the noisy `unmatched_initiative:` flag.

- [ ] **Step 1: Write failing test**

```python
# tests/test_brief.py
from app.schemas.research import Initiative, MappedInitiative
from app.services.brief import assemble_brief


def _init(text: str) -> Initiative:
    return Initiative(initiative=text, evidence="e", source_url="https://x")


def test_brief_flags_unverified_capability():
    mapped = [
        MappedInitiative(
            initiative=_init("Three-Phase QC push"),
            matched_capability=None,
            match_reason="not offered",
            unverified_capability="three_phase_control",
        )
    ]
    brief = assemble_brief(
        signals=[], initiatives=[_init("x")], mapped=mapped,
        gaps=[], questions=[], angle="",
    )
    assert "capability_unverified: three_phase_control" in brief.flags


def test_brief_flags_deduped():
    mapped = [
        MappedInitiative(
            initiative=_init(f"i{n}"),
            matched_capability=None,
            match_reason="",
            unverified_capability="three_phase_control",
        )
        for n in range(2)
    ]
    brief = assemble_brief(
        signals=[], initiatives=[_init("x")], mapped=mapped,
        gaps=[], questions=[], angle="",
    )
    assert brief.flags.count("capability_unverified: three_phase_control") == 1


def test_brief_status_failed_when_no_initiatives():
    brief = assemble_brief(
        signals=[], initiatives=[], mapped=[], gaps=[], questions=[], angle="",
    )
    assert brief.status == "failed"
```

- [ ] **Step 2: Run tests, verify failure**

Run: `pytest tests/test_brief.py -v`
Expected: FAIL — current code emits `unmatched_initiative:` not `capability_unverified:`.

- [ ] **Step 3: Replace flag-building block in `brief.py`**

```python
    flags: list[str] = []
    seen: set[str] = set()
    for m in mapped:
        if m.unverified_capability:
            flag = f"capability_unverified: {m.unverified_capability}"
            if flag not in seen:
                seen.add(flag)
                flags.append(flag)
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_brief.py -v`
Expected: PASS all three.

- [ ] **Step 5: Commit**

```bash
git add app/services/brief.py tests/test_brief.py
git commit -m "feat(brief): roll unverified_capability into flags, dedupe"
```

---

### Task 4: Test capability-map loader + mapping

**Files:**
- Create: `tests/test_capabilities.py`

**Interfaces:**
- Consumes: `load_capability_map() -> CapabilityMap` from `app/services/capabilities.py`.
- Produces: no code changes — tests only. Verifies YAML shape stays valid and `map_capabilities` filters unknown capability names.

- [ ] **Step 1: Write tests**

```python
# tests/test_capabilities.py
from unittest.mock import patch

from app.schemas.research import Initiative
from app.services import capabilities as cap_mod


def test_capability_map_loads_from_yaml():
    cap_mod.load_capability_map.cache_clear()
    cmap = cap_mod.load_capability_map()
    assert len(cmap.capabilities) > 0
    assert any(c.id == "unified_inspection_view" for c in cmap.capabilities)
    assert any(n.id == "three_phase_control" for n in cmap.not_capabilities)


def test_map_capabilities_discards_unknown_match_name():
    init = Initiative(initiative="i", evidence="e", source_url="https://x")
    fake_llm = '{"mapped":[{"index":0,"matched_capability":"Made Up Cap","match_reason":"r"}]}'
    with patch("app.services.capabilities.call_llm", return_value=fake_llm):
        out = cap_mod.map_capabilities([init])
    assert out[0].matched_capability is None
    assert out[0].unverified_capability is None


def test_map_capabilities_accepts_valid_unverified_id():
    init = Initiative(initiative="i", evidence="e", source_url="https://x")
    fake_llm = (
        '{"mapped":[{"index":0,"matched_capability":null,'
        '"unverified_capability":"three_phase_control","match_reason":"r"}]}'
    )
    with patch("app.services.capabilities.call_llm", return_value=fake_llm):
        out = cap_mod.map_capabilities([init])
    assert out[0].unverified_capability == "three_phase_control"
```

- [ ] **Step 2: Run tests**

Run: `pytest tests/test_capabilities.py -v`
Expected: PASS all three.

- [ ] **Step 3: Commit**

```bash
git add tests/test_capabilities.py
git commit -m "test(capabilities): cover YAML load + name validation + flag path"
```

---

### Task 5: Live smoke test script

**Files:**
- Create: `scripts/smoke_apify.py`

**Interfaces:**
- Consumes: `.env` (`APIFY_API_KEY`, `APIFY_JOBS_ACTOR_ID`).
- Produces: prints signal count + first 3 job titles + fires full `run_research()` and dumps the `ResearchBrief` JSON to stdout. Manual invocation only — not run in pytest.

- [ ] **Step 1: Create script**

```python
# scripts/smoke_apify.py
"""Manual end-to-end smoke test. Usage: python scripts/smoke_apify.py <domain> [name]"""
import json
import sys

from app.schemas.research import ResearchRequest
from app.services.research import run_research
from app.services.signals import gather_signals


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: smoke_apify.py <domain> [name]", file=sys.stderr)
        return 2
    domain = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else None

    sigs = gather_signals(domain=domain, name=name)
    print(f"signals: {len(sigs)}")
    for s in sigs[:3]:
        first_line = s.text.split("\n", 1)[0]
        print(f"  [{s.type}] {first_line[:80]}")

    brief = run_research("smoke", ResearchRequest(domain=domain, name=name))
    print(json.dumps(brief.model_dump(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run against a real domain**

Run: `python scripts/smoke_apify.py greenhouse.io`
Expected: prints ≥1 signal, then a `ResearchBrief` JSON. If `ANTHROPIC_API_KEY` is unset, initiatives/gaps/questions/angle will be empty but signals + sources should populate.

- [ ] **Step 3: Verify cost**

Check https://console.apify.com/billing — one run should cost ≤ $0.10.

- [ ] **Step 4: Commit**

```bash
git add scripts/smoke_apify.py
git commit -m "chore: add manual apify smoke script"
```

---

### Task 6: Update existing test to reflect flag change

**Files:**
- Modify: `tests/test_research.py`

**Interfaces:**
- No code changes. This task makes sure the pre-existing test still passes after Task 3's flag rename.

- [ ] **Step 1: Run existing suite**

Run: `pytest tests/test_research.py -v`
Expected: PASS. Both tests already only check `status`, `initiatives`, `gaps`, and top-level keys — they should be unaffected. If they fail, fix by adjusting the test to match the new flag format (do NOT re-introduce the old flag).

- [ ] **Step 2: Full suite green**

Run: `pytest -q`
Expected: all tests PASS.

- [ ] **Step 3: Commit only if changes needed**

```bash
# if tests/test_research.py was modified:
git add tests/test_research.py
git commit -m "test(research): align with capability_unverified flag"
```

---

## Self-Review

- **Spec coverage:**
  - PRD §7 domain-anchored input → Task 1 (`domainFilter`).
  - PRD §8 job-posting-weighted signals → Task 2 (title+description mapped).
  - PRD §12 no-fabricated-capability guardrail → Task 3 + Task 4 (flag rollup + name validation).
  - PRD §12 failure path → Task 3 (`status="failed"` when no initiatives).
  - Pipeline-steps build order step 3 (signals real) → Tasks 1+2.
  - Pipeline-steps step 5 (capability map) → Task 4 (already wired in prior work; test coverage added here).
  - Pipeline-steps step 8 (failure path) → covered by Task 3 + Task 6.
- **Placeholder scan:** no TBDs, all code shown inline.
- **Type consistency:** `MappedInitiative.unverified_capability: str | None` matches schema; `Signal(type="job_posting", url, text)` matches schema; `fetch_job_postings` signature stable across Tasks 1 and 2.
