from unittest.mock import patch

from app.schemas.research import JobFacts, Signal


def _sig(url, skills=None, date=None, salary_max=None):
    return Signal(
        type="job_posting", url=url, text=f"body-{url}",
        facts=JobFacts(
            skills=skills or [], date_posted=date, salary_max=salary_max,
        ),
    )


def test_infer_initiatives_orders_signals_recent_then_salary():
    captured = {}

    def fake_llm(system, user, **kw):
        captured["user"] = user
        return '{"initiatives": []}'

    old = _sig("https://a", date="2025-01-01", salary_max=100000)
    new_hi = _sig("https://b", date="2026-08-01", salary_max=200000)
    new_lo = _sig("https://c", date="2026-08-01", salary_max=80000)

    with patch("app.services.initiatives.call_llm", side_effect=fake_llm):
        from app.services import initiatives
        initiatives.infer_initiatives([old, new_hi, new_lo])

    body = captured["user"]
    # Most recent + highest salary should appear before older ones.
    assert body.index("https://b") < body.index("https://a")
    assert body.index("https://c") < body.index("https://a")
    # Same date, higher salary first.
    assert body.index("https://b") < body.index("https://c")


def test_infer_initiatives_stable_when_facts_missing():
    signals = [
        Signal(type="news", url="https://n1", text="x"),
        Signal(type="news", url="https://n2", text="y"),
    ]
    captured = {}

    def fake_llm(system, user, **kw):
        captured["user"] = user
        return '{"initiatives": []}'

    with patch("app.services.initiatives.call_llm", side_effect=fake_llm):
        from app.services import initiatives
        initiatives.infer_initiatives(signals)

    body = captured["user"]
    assert body.index("https://n1") < body.index("https://n2")
