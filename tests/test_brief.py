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
