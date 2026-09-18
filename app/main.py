from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import health, research

# Public API metadata is a constant, never sourced from env. A misconfigured
# variable reaching app_name would otherwise be published in /openapi.json
# and /docs, both of which are unauthenticated.
API_TITLE = "account-intelligence"

app = FastAPI(title=API_TITLE, version=settings.version)

app.include_router(health.router)
app.include_router(research.router)

app.mount("/ui", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="ui")


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """Send visitors to the UI; the bare host is not a useful landing page."""
    return RedirectResponse(url="/ui/", status_code=307)


@app.get("/version")
def version() -> dict[str, str]:
    """Version only.

    This previously lived on / and echoed settings.app_name too. Any
    misconfigured env var landing in app_name was then published on a public
    unauthenticated route, so no endpoint reflects configuration back now.
    """
    return {"version": settings.version}
