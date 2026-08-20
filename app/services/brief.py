from app.schemas.research import (
    DiscoveryQuestion,
    Gap,
    Initiative,
    MappedInitiative,
    ResearchBrief,
    Signal,
    Source,
)


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


def assemble_brief(
    signals: list[Signal],
    initiatives: list[Initiative],
    mapped: list[MappedInitiative],
    gaps: list[Gap],
    questions: list[DiscoveryQuestion],
    angle: str,
) -> ResearchBrief:
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

    flags: list[str] = []
    seen: set[str] = set()
    for m in mapped:
        if m.unverified_capability:
            f = f"capability_unverified: {m.unverified_capability}"
            if f not in seen:
                seen.add(f)
                flags.append(f)
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
