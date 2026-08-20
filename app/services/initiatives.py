import json

from app.clients.anthropic import call_llm, parse_json
from app.schemas.research import Initiative, Signal

INITIATIVES_SYSTEM_PROMPT = """
You are a sales research analyst. From the provided web signals (job postings, news,
site content), infer 2–5 concrete initiatives the company is pursuing.

Each initiative MUST include:
- initiative: short phrase, what they're trying to accomplish
- evidence: 1–2 sentences quoting/paraphrasing supporting signal
- source_url: URL of the single strongest supporting signal

Rules:
- Never invent facts not in the signals.
- If signals are thin, return fewer initiatives (or empty list).
- Weight job postings highest — they leak internal priorities.

Return JSON: {"initiatives": [{"initiative": "...", "evidence": "...", "source_url": "..."}]}
""".strip()


def _rank(sig):
    """Rank key for sorting: (date_posted, salary_max) both treated as descending."""
    facts = getattr(sig, "facts", None)
    date = (facts.date_posted if facts and facts.date_posted else "")
    salary = (facts.salary_max if facts and facts.salary_max else 0.0)
    return (date, salary)


def infer_initiatives(signals: list[Signal]) -> list[Initiative]:
    if not signals:
        return []

    # Sort signals by recency (date_posted desc), then salary (salary_max desc),
    # then original index (asc) to maintain stable sort.
    ordered = sorted(
        enumerate(signals),
        key=lambda p: (_rank(p[1]), -p[0]),
        reverse=True,
    )
    signals_ordered = [s for _, s in ordered]

    user = _format_signals(signals_ordered)
    raw = call_llm(system=INITIATIVES_SYSTEM_PROMPT, user=user)
    try:
        data = parse_json(raw)
        return [Initiative(**i) for i in data.get("initiatives", [])]
    except (json.JSONDecodeError, TypeError, ValueError):
        return []


def _format_signals(signals: list[Signal]) -> str:
    lines = []
    for s in signals:
        lines.append(f"[{s.type}] {s.url}\n{s.text[:6000]}\n---")
    return "\n".join(lines)
