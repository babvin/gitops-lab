from fastapi import FastAPI

from sample_api.api.routes import health
from sample_api.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.service_name, version=settings.version)
    app.include_router(health.router)
    return app


app = create_app()
