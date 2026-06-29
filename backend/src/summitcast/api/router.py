from fastapi import APIRouter
from .strava import router as route
from .weather import router as weather

api_router = APIRouter()

# api_router.include_router(strava_router, prefix="/strava")
api_router.include_router(route, prefix="/strava")
api_router.include_router(weather, prefix="/weather")

@api_router.get("/health")
def health():
    return {"status": "ok"}
