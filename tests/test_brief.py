from app.schemas.research import Initiative, JobFacts, MappedInitiative, Signal
from app.services.brief import assemble_brief


def _init(text: str) -> Initiative:
    return Initiative(initiative=text, evidence="e", source_url="https://x")


def test_brief_source_carries_salary_and_skills_for_jobs():
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


def test_format_salary_range_single_min_only():
    from app.schemas.research import JobFacts
    from app.services.brief import _format_salary_range
    f = JobFacts(salary_min=120000, salary_currency="USD", salary_unit="YEAR")
    assert _format_salary_range(f) == "120000 USD/YEAR"


def test_format_salary_range_single_max_only():
    from app.schemas.research import JobFacts
    from app.services.brief import _format_salary_range
    f = JobFacts(salary_max=165000, salary_currency="USD", salary_unit="YEAR")
    assert _format_salary_range(f) == "165000 USD/YEAR"


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
