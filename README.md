# account-intelligence

API-only service (FastAPI).

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
make dev
```

Open http://localhost:8000/docs

## Commands

- `make dev` — reload server
- `make test` — pytest + coverage
- `make lint` — ruff
- `make fmt` — format + autofix
- `make typecheck` — mypy
- `make docker-run` — compose up

## Layout

```
app/
  main.py         # FastAPI app
  config.py       # settings via pydantic-settings
  routers/        # route modules
  schemas/        # pydantic models
tests/
```
