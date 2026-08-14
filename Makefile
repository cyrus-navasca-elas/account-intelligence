.PHONY: install dev test lint fmt typecheck run docker-build docker-run clean

install:
	pip install -e ".[dev]"

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

test:
	pytest --cov=app --cov-report=term-missing

lint:
	ruff check app tests

fmt:
	ruff format app tests
	ruff check --fix app tests

typecheck:
	mypy app

docker-build:
	docker build -t account-intelligence .

docker-run:
	docker compose up --build

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov dist build
