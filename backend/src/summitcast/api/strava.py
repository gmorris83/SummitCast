from fastapi import APIRouter, HTTPException, Query
import re
from summitcast.services.strava_service import get_strava_route

router = APIRouter()


# @router.get("/route/{strava_route_url}")
# def get_route(strava_route_url: str):
#     try:
#         print(f"Received request for Strava route: {strava_route_url}")
#         route_id = extract_route_id()
#         return get_strava_route(strava_route_url)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


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
    """
    Accepts either:
      - /api/route?route=123456789
      - /api/route?route=https://www.strava.com/routes/123456789
    Returns the numeric route ID.
    """
    route_id = extract_route_id(route)
    if not route_id:
        raise HTTPException(status_code=400, detail="Invalid Strava route URL or ID")

    try:
        print(f"Received request for Strava route: {route_id}")
        return get_strava_route(route_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

