from fastapi import APIRouter, HTTPException

from summitcast.services.weather_service import add_weather_to_route

router = APIRouter()


@router.post("")
def add_weather(data: dict):
    try:
        return add_weather_to_route(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
