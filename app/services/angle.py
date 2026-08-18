from app.clients.anthropic import call_llm
from app.schemas.research import Gap

ANGLE_SYSTEM_PROMPT = """
You are a sales strategist. Given a list of gaps, pick the STRONGEST one and write a
2–3 sentence outreach angle: the wedge to open the conversation.

Rules:
- Ground in the gap's evidence + impact.
- No pitch. No feature dump. Frame the problem.
- Plain prose. No JSON.
""".strip()


def pick_angle(gaps: list[Gap]) -> str:
    if not gaps:
        return ""
    user = "\n".join(
        f"- gap: {g.gap} | impact: {g.impact_hypothesis} | capability: {g.mapped_capability}"
        for g in gaps
    )
    return call_llm(system=ANGLE_SYSTEM_PROMPT, user=user).strip()
