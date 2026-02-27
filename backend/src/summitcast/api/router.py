from fastapi import APIRouter
from .routes_strava import router as strava_router

api_router = APIRouter()

api_router.include_router(strava_router, prefix="/strava")

@api_router.get("/health")
def health():
    return {"status": "ok"}
