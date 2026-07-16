from fastapi import APIRouter, Depends

from sample_api.core.config import Settings, get_settings
from sample_api.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/healthz", response_model=HealthResponse)
def healthz(settings: Settings = Depends(get_settings)) -> HealthResponse:
    """Liveness/readiness probe target. Cheap and dependency-free on purpose --
    add real downstream checks (DB, cache, etc.) here as the service grows,
    but keep the default path fast."""
    return HealthResponse(status="ok", service=settings.service_name, version=settings.version)
