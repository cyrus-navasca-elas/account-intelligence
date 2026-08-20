import json
import re
from typing import Any

from app.config import settings


def parse_json(raw: str) -> Any:
    """Parse LLM JSON output, tolerating code fences and prose wrappers."""
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    for open_c, close_c in (("{", "}"), ("[", "]")):
        start = text.find(open_c)
        end = text.rfind(close_c)
        if start != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                continue
    raise json.JSONDecodeError("no JSON payload found", raw, 0)


def call_llm(system: str, user: str, max_tokens: int = 4096) -> str:
    """Call Anthropic. Returns raw text response.

    TODO: implement real Anthropic SDK call once ANTHROPIC_API_KEY set.
    """
    if not settings.anthropic_api_key:
        return "{}"

    from anthropic import Anthropic

    client = Anthropic(api_key=settings.anthropic_api_key)
    resp = client.messages.create(
        model=settings.anthropic_model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return resp.content[0].text  # type: ignore[union-attr]
