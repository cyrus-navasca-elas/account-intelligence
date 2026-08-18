from app.clients import apify, web_search
from app.schemas.research import Signal


def gather_signals(domain: str | None, name: str | None) -> list[Signal]:
    """Collect raw materials for LLM interpretation. No LLM reasoning here."""
    signals: list[Signal] = []

    if domain:
        jobs = apify.fetch_job_postings(domain, name)
        for j in jobs:
            desc = str(j.get("description_text") or "").strip()
            if not desc:
                continue
            title = str(j.get("title") or "").strip()
            url = str(j.get("url") or "")
            text = f"{title}\n\n{desc}" if title else desc
            signals.append(Signal(type="job_posting", url=url, text=text))

    if name:
        web = web_search.search_company_signals(name, domain)
        for w in web:
            signals.append(Signal(type=w["type"], url=w["url"], text=w["content"]))

    return signals
