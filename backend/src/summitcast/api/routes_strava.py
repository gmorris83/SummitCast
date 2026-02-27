from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

router = APIRouter()


# Request model
class StravaForecastRequest(BaseModel):
    url: HttpUrl


# Response model
class StravaForecastResponse(BaseModel):
    eta: str
    forecast: str


@router.post("/forecast", response_model=StravaForecastResponse)
async def forecast_route(request: StravaForecastRequest):
    strava_url = request.url

    # TODO: Replace with real Strava route parsing & weather logic
    if "strava.com" not in strava_url:
        raise HTTPException(status_code=400, detail="Invalid Strava URL")

    # Dummy forecast
    return StravaForecastResponse(
        eta="1h 45m",
        forecast="Sunny with light clouds"
    )