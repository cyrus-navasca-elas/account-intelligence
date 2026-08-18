from app.config import settings


def fetch_job_postings(domain: str, name: str | None = None) -> list[dict]:
    """Fetch job postings for a company via Apify.

    TODO: pick actor, wire real run_input once APIFY_JOBS_ACTOR_ID set.
    Returns raw dataset items.
    """
    if not settings.apify_api_key or not settings.apify_jobs_actor_id:
        return []

    from apify_client import ApifyClient

    client = ApifyClient(settings.apify_api_key)
    run = client.actor(settings.apify_jobs_actor_id).call(
        run_input={"domain": domain, "companyName": name}
    )
    if not run:
        return []
    return list(client.dataset(run["defaultDatasetId"]).iterate_items())
