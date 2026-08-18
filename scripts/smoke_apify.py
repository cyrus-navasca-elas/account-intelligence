# scripts/smoke_apify.py
"""Manual end-to-end smoke test. Usage: python scripts/smoke_apify.py <domain> [name]"""
import json
import sys

from app.schemas.research import ResearchRequest
from app.services.research import run_research
from app.services.signals import gather_signals


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: smoke_apify.py <domain> [name]", file=sys.stderr)
        return 2
    domain = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else None

    sigs = gather_signals(domain=domain, name=name)
    print(f"signals: {len(sigs)}")
    for s in sigs[:3]:
        first_line = s.text.split("\n", 1)[0]
        print(f"  [{s.type}] {first_line[:80]}")

    brief = run_research("smoke", ResearchRequest(domain=domain, name=name))
    print(json.dumps(brief.model_dump(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
