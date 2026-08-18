from app.config import settings


def fetch_job_postings(
    domain: str,
    name: str | None = None,
    *,
    limit: int = 25,
    time_range: str = "6m",
) -> list[dict]:
    """Fetch recent job postings for a company via the career-site actor.

    Returns raw dataset items exactly as the actor emits them.
    """
    if not settings.apify_api_key or not settings.apify_jobs_actor_id:
        return []

    from apify_client import ApifyClient

    client = ApifyClient(settings.apify_api_key)
    run_input: dict = {
        "domainFilter": [domain],
        "timeRange": time_range,
        "limit": limit,
        "descriptionType": "text",
    }
    run = client.actor(settings.apify_jobs_actor_id).call(run_input=run_input)
    if not run:
        return []
    return list(client.dataset(run["defaultDatasetId"]).iterate_items())
