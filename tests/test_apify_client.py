from unittest.mock import MagicMock, patch


def test_fetch_job_postings_builds_correct_run_input():
    from app.clients import apify

    fake_actor = MagicMock()
    fake_actor.call.return_value = {"defaultDatasetId": "ds1"}
    fake_client = MagicMock()
    fake_client.actor.return_value = fake_actor
    fake_client.dataset.return_value.iterate_items.return_value = iter([])

    with patch("apify_client.ApifyClient", return_value=fake_client), \
         patch.object(apify.settings, "apify_api_key", "k"), \
         patch.object(apify.settings, "apify_jobs_actor_id", "fantastic-jobs/career-site-job-listing-api"):
        apify.fetch_job_postings("prospect.com")

    fake_client.actor.assert_called_once_with("fantastic-jobs/career-site-job-listing-api")
    (kwargs,) = fake_actor.call.call_args_list
    ri = kwargs.kwargs["run_input"]
    assert ri["domainFilter"] == ["prospect.com"]
    assert ri["timeRange"] == "6m"
    assert ri["limit"] == 25
    assert ri["descriptionType"] == "text"


def test_fetch_job_postings_returns_empty_without_key():
    from app.clients import apify
    with patch.object(apify.settings, "apify_api_key", ""):
        assert apify.fetch_job_postings("prospect.com") == []
