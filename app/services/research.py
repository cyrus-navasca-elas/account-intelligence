from app.schemas.research import ResearchBrief, ResearchRequest
from app.services import angle, brief, capabilities, gaps, initiatives, questions, reach_out, signals


def run_research(company_id: str, req: ResearchRequest) -> ResearchBrief:
    """Orchestrate the full pipeline. Sync for v0."""
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
