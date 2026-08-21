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

    if not gaps:
        return "hold", "No capability gaps synthesized despite mapped capabilities."

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
