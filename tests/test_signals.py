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


def test_gather_signals_packs_ai_fields_into_text():
    fake_jobs = [
        {
            "url": "https://x/y",
            "title": "QC Manager",
            "description_text": "Full JD body here.",
            "date_posted": "2026-08-10",
            "locations_derived": ["Tacoma, WA, USA"],
            "ai_salary_min_value": 120000,
            "ai_salary_max_value": 165000,
            "ai_salary_currency": "USD",
            "ai_salary_unit_text": "YEAR",
            "ai_experience_level": "10+",
            "ai_work_arrangement": "On-site",
            "ai_employment_type": ["FULL_TIME"],
            "ai_key_skills": ["Three-Phase Control", "USACE Compliance"],
            "ai_keywords": ["NAVFAC", "DFOW"],
            "ai_core_responsibilities": "Lead QC program.",
            "ai_requirements_summary": "10+ years USACE.",
        }
    ]
    with patch("app.services.signals.apify.fetch_job_postings", return_value=fake_jobs), \
         patch("app.services.signals.web_search.search_company_signals", return_value=[]):
        from app.services import signals
        out = signals.gather_signals(domain="prospect.com", name="X")

    text = out[0].text
    assert "QC Manager" in text
    assert "Tacoma, WA, USA" in text
    assert "salary=120000-165000 USD YEAR" in text
    assert "level=10+" in text
    assert "arrangement=On-site" in text
    assert "Skills: Three-Phase Control, USACE Compliance" in text
    assert "Keywords: NAVFAC, DFOW" in text
    assert "Responsibilities: Lead QC program." in text
    assert "Requirements: 10+ years USACE." in text
    assert "Full JD body here." in text


def test_gather_signals_populates_structured_job_facts():
    fake_jobs = [
        {
            "url": "https://x/y",
            "title": "QCM",
            "description_text": "Body.",
            "date_posted": "2026-07-28T17:15:46",
            "ai_salary_min_value": 120000,
            "ai_salary_max_value": 165000,
            "ai_salary_currency": "USD",
            "ai_salary_unit_text": "YEAR",
            "ai_key_skills": ["Three-Phase Control", "USACE Compliance"],
        }
    ]
    with patch("app.services.signals.apify.fetch_job_postings", return_value=fake_jobs), \
         patch("app.services.signals.web_search.search_company_signals", return_value=[]):
        from app.services import signals
        out = signals.gather_signals(domain="prospect.com", name=None)
    f = out[0].facts
    assert f is not None
    assert f.salary_min == 120000
    assert f.salary_max == 165000
    assert f.salary_currency == "USD"
    assert f.salary_unit == "YEAR"
    assert f.skills == ["Three-Phase Control", "USACE Compliance"]
    assert f.date_posted == "2026-07-28T17:15:46"


def test_gather_signals_facts_absent_fields_default():
    fake_jobs = [{"url": "https://x/y", "title": "T", "description_text": "b"}]
    with patch("app.services.signals.apify.fetch_job_postings", return_value=fake_jobs), \
         patch("app.services.signals.web_search.search_company_signals", return_value=[]):
        from app.services import signals
        out = signals.gather_signals(domain="prospect.com", name=None)
    f = out[0].facts
    assert f is not None
    assert f.salary_min is None and f.salary_max is None
    assert f.skills == []
    assert f.date_posted is None


def test_gather_signals_omits_absent_ai_fields():
    fake_jobs = [
        {
            "url": "https://x/y",
            "title": "Estimator",
            "description_text": "Body.",
        }
    ]
    with patch("app.services.signals.apify.fetch_job_postings", return_value=fake_jobs), \
         patch("app.services.signals.web_search.search_company_signals", return_value=[]):
        from app.services import signals
        out = signals.gather_signals(domain="prospect.com", name=None)
    text = out[0].text
    assert "salary=" not in text
    assert "Skills:" not in text
    assert "Keywords:" not in text
    assert "Estimator" in text
    assert "Body." in text
