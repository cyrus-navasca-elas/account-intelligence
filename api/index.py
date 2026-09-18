"""Vercel serverless entrypoint.

Vercel's Python runtime looks for an ASGI `app` in this module. All real
wiring stays in app/main.py so the container and serverless paths run the
exact same application.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app  # noqa: E402

__all__ = ["app"]
