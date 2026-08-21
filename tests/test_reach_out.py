from unittest.mock import patch

from app.schemas.research import Gap, Initiative, JobFacts, MappedInitiative, Signal


def _init(txt="i"):
    return Initiative(initiative=txt, evidence="e", source_url="https://x")


def _mapped(cap=None):
    return MappedInitiative(initiative=_init(), matched_capability=cap, match_reason="r")


def _gap(cap="One live view of every inspection"):
    return Gap(gap="g", mapped_capability=cap, impact_hypothesis="h", initiative_ref=0)


def test_reach_out_deterministic_skip_when_failed():
    from app.services.reach_out import decide_reach_out
    r, reason = decide_reach_out(
        status="failed", signals=[], mapped=[], gaps=[], angle="",
    )
    assert r == "skip"
    assert "no signals" in reason.lower()


def test_reach_out_deterministic_skip_when_no_mapped_gaps():
    from app.services.reach_out import decide_reach_out
    r, reason = decide_reach_out(
        status="enriched",
        signals=[Signal(type="news", url="a", text="b")],
        mapped=[_mapped(cap=None)],
        gaps=[],
        angle="",
    )
    assert r == "skip"
    assert "no elas capability" in reason.lower()


def test_reach_out_calls_llm_when_gaps_present():
    from app.services import reach_out as ro
    fake = '{"recommendation":"yes","reason":"strong gap fit"}'
    sig = Signal(
        type="job_posting", url="https://x", text="b",
        facts=JobFacts(date_posted="2026-08-01"),
    )
    with patch("app.services.reach_out.call_llm", return_value=fake) as m:
        r, reason = ro.decide_reach_out(
            status="enriched",
            signals=[sig],
            mapped=[_mapped(cap="One live view of every inspection")],
            gaps=[_gap()],
            angle="wedge",
        )
    assert r == "yes"
    assert reason == "strong gap fit"
    assert m.call_count == 1


def test_reach_out_falls_back_to_hold_on_bad_json():
    from app.services import reach_out as ro
    with patch("app.services.reach_out.call_llm", return_value="not json"):
        r, reason = ro.decide_reach_out(
            status="enriched", signals=[], mapped=[_mapped(cap="X")], gaps=[_gap()],
            angle="w",
        )
    assert r == "hold"
    assert "unavailable" in reason.lower()


def test_reach_out_normalizes_unknown_recommendation_to_hold():
    from app.services import reach_out as ro
    fake = '{"recommendation":"maybe","reason":"unclear"}'
    with patch("app.services.reach_out.call_llm", return_value=fake):
        r, _ = ro.decide_reach_out(
            status="enriched", signals=[], mapped=[_mapped(cap="X")], gaps=[_gap()],
            angle="w",
        )
    assert r == "hold"


def test_reach_out_holds_when_mapped_but_no_gaps_synthesized():
    from app.services.reach_out import decide_reach_out
    r, reason = decide_reach_out(
        status="enriched",
        signals=[],
        mapped=[_mapped(cap="One live view of every inspection")],
        gaps=[],
        angle="",
    )
    assert r == "hold"
    assert "no capability gaps" in reason.lower()
