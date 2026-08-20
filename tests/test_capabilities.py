from unittest.mock import patch

from app.schemas.research import Initiative
from app.services import capabilities as cap_mod


def test_capability_map_loads_from_yaml():
    cap_mod.load_capability_map.cache_clear()
    cmap = cap_mod.load_capability_map()
    assert len(cmap.capabilities) > 0
    assert any(c.id == "unified_inspection_view" for c in cmap.capabilities)
    assert any(n.id == "three_phase_control" for n in cmap.not_capabilities)


def test_map_capabilities_discards_unknown_match_name():
    init = Initiative(initiative="i", evidence="e", source_url="https://x")
    fake_llm = '{"mapped":[{"index":0,"matched_capability":"Made Up Cap","match_reason":"r"}]}'
    with patch("app.services.capabilities.call_llm", return_value=fake_llm):
        out = cap_mod.map_capabilities([init])
    assert out[0].matched_capability is None
    assert out[0].unverified_capability is None


def test_map_capabilities_accepts_valid_unverified_id():
    init = Initiative(initiative="i", evidence="e", source_url="https://x")
    fake_llm = (
        '{"mapped":[{"index":0,"matched_capability":null,'
        '"unverified_capability":"three_phase_control","match_reason":"r"}]}'
    )
    with patch("app.services.capabilities.call_llm", return_value=fake_llm):
        out = cap_mod.map_capabilities([init])
    assert out[0].unverified_capability == "three_phase_control"


def test_detect_flags_from_skills_matches_three_phase_control():
    from app.schemas.research import JobFacts, Signal
    from app.services.capabilities import detect_flags_from_skills, load_capability_map

    load_capability_map.cache_clear()
    cmap = load_capability_map()
    signals = [
        Signal(
            type="job_posting",
            url="https://x/y",
            text="body",
            facts=JobFacts(skills=["Three-Phase Control Process", "USACE Compliance"]),
        )
    ]
    flags = detect_flags_from_skills(signals, cmap)
    assert "capability_unverified: three_phase_control" in flags


def test_detect_flags_dedupes_across_signals():
    from app.schemas.research import JobFacts, Signal
    from app.services.capabilities import detect_flags_from_skills, load_capability_map

    load_capability_map.cache_clear()
    cmap = load_capability_map()
    sigs = [
        Signal(type="job_posting", url="a", text="", facts=JobFacts(skills=["USACE"])),
        Signal(type="job_posting", url="b", text="", facts=JobFacts(skills=["NAVFAC", "DFOW"])),
    ]
    flags = detect_flags_from_skills(sigs, cmap)
    assert flags.count("capability_unverified: three_phase_control") == 1


def test_detect_flags_ignores_signals_without_facts():
    from app.schemas.research import Signal
    from app.services.capabilities import detect_flags_from_skills, load_capability_map

    load_capability_map.cache_clear()
    cmap = load_capability_map()
    sigs = [Signal(type="news", url="a", text="Three-Phase Control mentioned in prose")]
    assert detect_flags_from_skills(sigs, cmap) == []


def test_detect_flags_ignores_non_job_posting_signals_even_if_facts_present():
    from app.schemas.research import JobFacts, Signal
    from app.services.capabilities import detect_flags_from_skills, load_capability_map
    load_capability_map.cache_clear()
    cmap = load_capability_map()
    sigs = [Signal(type="news", url="https://n", text="",
                   facts=JobFacts(skills=["Three-Phase Control"]))]
    assert detect_flags_from_skills(sigs, cmap) == []
