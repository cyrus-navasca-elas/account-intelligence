import json

from app.clients.anthropic import call_llm
from app.schemas.research import DiscoveryQuestion, Gap

QUESTIONS_SYSTEM_PROMPT = """
You are a gap-selling coach. For each gap, generate discovery questions covering
these stages (produce 1 per stage where it makes sense):
- current_state
- current_state_impact
- org_strain
- root_cause
- future_state
- gap_question

Rules:
- Questions are open-ended, tied to the gap.
- No leading questions. No pitching.
- gap_ref must match the input gap index.

Return JSON: {"questions": [{"gap_ref": 0, "stage": "current_state", "question": "..."}]}
""".strip()


def generate_questions(gaps: list[Gap]) -> list[DiscoveryQuestion]:
    if not gaps:
        return []

    user = _format(gaps)
    raw = call_llm(system=QUESTIONS_SYSTEM_PROMPT, user=user)

    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError, ValueError):
        return []

    out: list[DiscoveryQuestion] = []
    for q in data.get("questions", []):
        try:
            out.append(DiscoveryQuestion(**q))
        except (TypeError, ValueError):
            continue
    return out


def _format(gaps: list[Gap]) -> str:
    return "\n".join(
        f"[{i}] gap: {g.gap} | impact: {g.impact_hypothesis} | capability: {g.mapped_capability}"
        for i, g in enumerate(gaps)
    )
