from fastapi import APIRouter, HTTPException, Query
import re
from summitcast.services.strava_service import StravaService

router = APIRouter()


def extract_route_id(url_or_id: str) -> str | None:
    """
    Accepts a full Strava route URL or a numeric ID.
    Returns the numeric route ID as a string, or None if invalid.
    """
    # Check if it's already numeric
    if url_or_id.isdigit():
        return url_or_id

        # Otherwise try to extract from URL
    match = re.search(r'/routes/(\d+)', url_or_id)
    if match:
        return match.group(1)
    return None


@router.get("/route")
def get_route(route: str = Query(..., description="Strava route URL or numeric ID")):
    route_id = extract_route_id(route)
    if not route_id:
        raise HTTPException(status_code=400, detail="Invalid Strava route URL or ID")

    strava_service = StravaService(route_id)

    try:
        print(f"Received request for Strava route: {route_id}")
        return strava_service.get_strava_route()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

