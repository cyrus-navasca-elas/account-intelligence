from app.schemas.research import (
    DiscoveryQuestion,
    Gap,
    Initiative,
    MappedInitiative,
    ResearchBrief,
    Signal,
    Source,
)


def assemble_brief(
    signals: list[Signal],
    initiatives: list[Initiative],
    mapped: list[MappedInitiative],
    gaps: list[Gap],
    questions: list[DiscoveryQuestion],
    angle: str,
) -> ResearchBrief:
    sources = [Source(type=s.type, url=s.url, summary=s.text[:200]) for s in signals]

    flags: list[str] = []
    seen: set[str] = set()
    for m in mapped:
        if m.unverified_capability:
            flag = f"capability_unverified: {m.unverified_capability}"
            if flag not in seen:
                seen.add(flag)
                flags.append(flag)

    status = "enriched" if initiatives else "failed"
    current_state = _summarize_current_state(initiatives)

    return ResearchBrief(
        status=status,
        current_state=current_state,
        initiatives=initiatives,
        gaps=gaps,
        discovery_questions=questions,
        recommended_angle=angle,
        sources=sources,
        flags=flags,
    )


def _summarize_current_state(initiatives: list[Initiative]) -> str:
    if not initiatives:
        return ""
    return " ".join(i.evidence for i in initiatives[:3])
