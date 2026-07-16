IMAGE ?= ghcr.io/<GITHUB_OWNER>/sample-api
TAG   ?= dev

.PHONY: install lint format test run docker-build docker-run clean

install:
	uv sync --dev

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .
	uv run ruff check --fix .

test:
	uv run pytest

run:
	uv run uvicorn sample_api.main:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -t $(IMAGE):$(TAG) .

docker-run:
	docker run --rm -p 8000:8000 $(IMAGE):$(TAG)

clean:
	rm -rf .venv .pytest_cache .ruff_cache
