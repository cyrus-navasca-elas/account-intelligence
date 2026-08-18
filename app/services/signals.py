from app.clients import apify, tavily
from app.schemas.research import Signal


def gather_signals(domain: str | None, name: str | None) -> list[Signal]:
    """Collect raw materials for LLM interpretation. No LLM here."""
    signals: list[Signal] = []

    if domain:
        jobs = apify.fetch_job_postings(domain, name)
        for j in jobs:
            signals.append(
                Signal(
                    type="job_posting",
                    url=str(j.get("url", "")),
                    text=str(j.get("description", "") or j.get("text", "")),
                )
            )

    if name:
        news = tavily.search_news(name)
        for n in news:
            signals.append(
                Signal(
                    type="news",
                    url=str(n.get("url", "")),
                    text=str(n.get("content", "")),
                )
            )

    if domain:
        site_text = tavily.fetch_site(f"https://{domain}")
        if site_text:
            signals.append(Signal(type="site", url=f"https://{domain}", text=site_text))

    return signals
