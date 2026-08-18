import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_signals():
    """Patch signal gathering to prevent network calls in all tests."""
    with patch("app.services.signals.apify.fetch_job_postings", return_value=[]), \
         patch("app.services.signals.tavily.search_news", return_value=[]), \
         patch("app.services.signals.tavily.fetch_site", return_value=""):
        yield


def test_research_no_input_returns_failed_brief():
    r = client.post("/research/companies/test-1", json={})
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "failed"
    assert body["initiatives"] == []
    assert body["gaps"] == []


def test_research_schema_shape():
    r = client.post("/research/companies/test-2", json={"domain": "example.com"})
    assert r.status_code == 200
    body = r.json()
    for key in [
        "status",
        "current_state",
        "initiatives",
        "gaps",
        "discovery_questions",
        "recommended_angle",
        "sources",
        "flags",
    ]:
        assert key in body
