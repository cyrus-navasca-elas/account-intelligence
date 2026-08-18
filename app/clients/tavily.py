from app.config import settings


def search_news(query: str, max_results: int = 5) -> list[dict]:
    """Search news via Tavily. Returns list of {title, url, content}.

    TODO: swap topic/depth once tuned for use case.
    """
    if not settings.tavily_api_key:
        return []

    from tavily import TavilyClient

    client = TavilyClient(api_key=settings.tavily_api_key)
    resp = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
        topic="news",
    )
    return list(resp.get("results", []))


def fetch_site(url: str) -> str:
    """Fetch and extract site content via Tavily extract."""
    if not settings.tavily_api_key:
        return ""

    from tavily import TavilyClient

    client = TavilyClient(api_key=settings.tavily_api_key)
    resp = client.extract(urls=[url])
    results = resp.get("results", [])
    if not results:
        return ""
    return str(results[0].get("raw_content", ""))
