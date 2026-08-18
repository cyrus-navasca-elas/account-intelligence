from app.config import settings


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
