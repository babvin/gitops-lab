# sample-api

Minimal FastAPI service used to prove out the ArgoCD-managed path of the
GitOps lab end-to-end: real source, real tests, real CI, real image, real
deployment -- not just a static nginx placeholder.

## Layout

```
sample-api/
├── src/sample_api/
│   ├── main.py              # FastAPI app factory
│   ├── api/routes/health.py # GET /healthz
│   ├── core/config.py       # env-driven settings (pydantic-settings)
│   └── schemas/health.py
├── tests/                   # pytest + FastAPI TestClient
├── deploy/                  # Deployment/Service/Kustomization -- ArgoCD's source
├── Dockerfile                # multi-stage, uv-based, non-root runtime
├── Makefile
└── pyproject.toml            # deps + ruff + pytest config, uv-managed
```

## Local dev

```
make install   # uv sync --dev
make lint      # ruff check + format --check
make test      # pytest
make run       # uvicorn --reload on :8000
```

## CI

`.github/workflows/sample-api-ci.yml` (repo root -- GitHub Actions can't read
workflows from subdirectories) lints, tests, and builds a Docker image on
every PR touching this path; on push to `main` it also pushes to
`ghcr.io/<owner>/sample-api:latest` and `:<sha>` for both amd64 and arm64 platforms.

**What CI does *not* do yet:** write the new image tag back into
`deploy/kustomization.yaml`. Right now that's a manual step:

```
cd deploy && kustomize edit set image ghcr.io/<owner>/sample-api=ghcr.io/<owner>/sample-api:<sha>
```

then commit and push -- ArgoCD picks it up from there. Automating that
write-back is a reasonable next step, either as a commit-back step in this
same workflow (needs `contents: write` and a loop-guard on the commit path)
or via ArgoCD Image Updater / Flux Image Automation watching the registry
directly instead of CI writing to Git.
