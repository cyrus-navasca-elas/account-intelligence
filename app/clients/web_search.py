import json
import re

from app.config import settings


def search_company_signals(name: str, domain: str | None) -> list[dict]:
    """Use Claude's server-side web_search to gather news + site signals.

    Returns list of {"type": "news"|"site", "url": str, "content": str}.
    """
    if not settings.anthropic_api_key:
        return []

    from anthropic import Anthropic

    client = Anthropic(api_key=settings.anthropic_api_key)

    site_hint = f" Their website is https://{domain}." if domain else ""
    user = (
        f"Research the company '{name}'.{site_hint}\n\n"
        "Use the web_search tool to find:\n"
        "1. Recent news, awards, press releases, contract wins.\n"
        "2. Content from their own site (about, services, initiatives).\n\n"
        "Return ONLY a JSON array. Each item must be: "
        '{"type": "news" or "site", "url": "<real url>", '
        '"content": "1-3 sentence factual excerpt grounded in the source"}. '
        "Never invent URLs or facts. If nothing usable, return []."
    )
    system = (
        "You are a research assistant. Use web_search when it helps. "
        "Output ONLY a valid JSON array. No prose. No code fences."
    )

    resp = client.messages.create(
        model=settings.anthropic_model,
        max_tokens=4096,
        system=system,
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}],
        messages=[{"role": "user", "content": user}],
    )

    text = ""
    for block in resp.content:
        if getattr(block, "type", None) == "text":
            text += getattr(block, "text", "")

    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1 or end <= start:
        return []
    try:
        data = json.loads(text[start : end + 1])
    except Exception:
        return []

    if not isinstance(data, list):
        return []

    out: list[dict] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        url = str(item.get("url", "")).strip()
        content = str(item.get("content", "")).strip()
        t = item.get("type", "news")
        if t not in ("news", "site"):
            t = "news"
        if url and content:
            out.append({"type": t, "url": url, "content": content})
    return out
