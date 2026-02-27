from fastapi import APIRouter
from summitcast.services.weather_service import get_weather_for_waypoints

router = APIRouter()

@router.post("/weather")
def weather(data: dict):
    return get_weather_for_waypoints(data)