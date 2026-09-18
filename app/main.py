from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import health, research

app = FastAPI(title=settings.app_name, version=settings.version)

app.include_router(health.router)
app.include_router(research.router)

app.mount("/ui", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="ui")


@app.get("/")
def root() -> dict[str, str]:
    """Root returns the version only.

    It previously echoed settings.app_name. Any misconfigured env var that
    lands in app_name is then published on a public unauthenticated route, so
    this endpoint no longer reflects configuration back to the caller.
    """
    return {"version": settings.version}
