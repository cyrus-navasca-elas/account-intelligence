import json

from app.clients.anthropic import call_llm
from app.schemas.research import Gap, MappedInitiative

GAPS_SYSTEM_PROMPT = """
You are a gap-selling analyst. For each initiative + matched ELAS capability,
produce ONE gap statement with:
- gap: concrete missing capability or process (short phrase)
- impact_hypothesis: what that gap likely costs them (1 sentence)

Rules:
- Ground the gap in the initiative's evidence.
- Never claim a capability ELAS doesn't have.
- If evidence is too thin, skip the initiative.

Return JSON: {"gaps": [{"initiative_ref": 0, "gap": "...", "impact_hypothesis": "..."}]}
""".strip()


def synthesize_gaps(mapped: list[MappedInitiative]) -> list[Gap]:
    matched = [(i, m) for i, m in enumerate(mapped) if m.matched_capability]
    if not matched:
        return []

    user = _format(matched)
    raw = call_llm(system=GAPS_SYSTEM_PROMPT, user=user)

    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError, ValueError):
        return []

    gaps: list[Gap] = []
    for g in data.get("gaps", []):
        ref = g.get("initiative_ref")
        if ref is None or ref >= len(mapped):
            continue
        cap = mapped[ref].matched_capability
        if not cap:
            continue
        gaps.append(
            Gap(
                gap=g.get("gap", ""),
                mapped_capability=cap,
                impact_hypothesis=g.get("impact_hypothesis", ""),
                initiative_ref=ref,
            )
        )
    return gaps


def _format(matched: list[tuple[int, MappedInitiative]]) -> str:
    lines = []
    for idx, m in matched:
        lines.append(
            f"[{idx}] initiative: {m.initiative.initiative}\n"
            f"    evidence: {m.initiative.evidence}\n"
            f"    matched_capability: {m.matched_capability}"
        )
    return "\n".join(lines)
