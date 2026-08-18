from unittest.mock import patch

from app.schemas.research import Signal


def test_gather_signals_maps_jobs_to_signals():
    fake_jobs = [
        {
            "url": "https://boards.greenhouse.io/x/jobs/1",
            "title": "QC Manager - NAVFAC",
            "description_text": "Own Three-Phase Control across $20M+ jobs.",
            "date_posted": "2026-08-10",
        }
    ]
    with patch("app.services.signals.apify.fetch_job_postings", return_value=fake_jobs), \
         patch("app.services.signals.web_search.search_company_signals", return_value=[]):
        from app.services import signals
        out = signals.gather_signals(domain="prospect.com", name="Prospect")

    assert len(out) == 1
    s = out[0]
    assert isinstance(s, Signal)
    assert s.type == "job_posting"
    assert s.url == "https://boards.greenhouse.io/x/jobs/1"
    assert "QC Manager - NAVFAC" in s.text
    assert "Three-Phase Control" in s.text


def test_gather_signals_skips_jobs_without_description():
    fake_jobs = [{"url": "https://x/y", "title": "T", "description_text": ""}]
    with patch("app.services.signals.apify.fetch_job_postings", return_value=fake_jobs), \
         patch("app.services.signals.web_search.search_company_signals", return_value=[]):
        from app.services import signals
        out = signals.gather_signals(domain="prospect.com", name=None)
    assert out == []
