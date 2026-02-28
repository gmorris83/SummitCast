from typing import Dict

import requests
from typing_extensions import Any

from summitcast.helpers import strava_tokens
from summitcast.assets.domains import Athlete, Waypoint, Segment, Route

def get_strava_route(route_id: str):
    print(f"Fetching Strava route from URL: {route_id}")

    url = f"https://www.strava.com/api/v3/routes/{route_id}"
    access_tokens = strava_tokens.get_valid_access_token()
    headers = {
        "Authorization": f"Bearer {access_tokens[0]}"
    }

    if not access_tokens:
        raise Exception("Missing STRAVA_ACCESS_TOKEN")

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    if response.status_code != 200:
        raise Exception(f"Strava API error: {response.text}")

    data = response.json()
    return parse_strava_route(data)

def parse_strava_route(data: Dict[str, Any]) -> Route:
    athlete_data = data["athlete"]

    athlete = Athlete(
        id=athlete_data["id"],
        username=athlete_data["username"],
        firstname=athlete_data["firstname"],
        lastname=athlete_data["lastname"],
        city=athlete_data.get("city"),
        country=athlete_data.get("country"),
        weight=athlete_data.get("weight"),
    )

    waypoints = [
        Waypoint(
            title=wp["title"],
            lat=wp["latlng"][0],
            lon=wp["latlng"][1],
            distance_into_route=wp["distance_into_route"],
            categories=wp.get("categories", []),
        )
        for wp in data.get("waypoints", [])
    ]

    segments = [
        Segment(
            id=seg["id"],
            name=seg["name"],
            distance=seg["distance"],
            average_grade=seg["average_grade"],
            max_grade=seg["maximum_grade"],
            elevation_high=seg["elevation_high"],
            elevation_low=seg["elevation_low"],
            start_latlng=tuple(seg["start_latlng"]),
            end_latlng=tuple(seg["end_latlng"]),
        )
        for seg in data.get("segments", [])
    ]

    route = Route(
        id=data["id"],
        name=data["name"],
        description=data.get("description", ""),
        distance=data["distance"],
        elevation_gain=data["elevation_gain"],
        estimated_moving_time=data["estimated_moving_time"],
        polyline=data["map"]["polyline"],
        athlete=athlete,
        waypoints=waypoints,
        segments=segments,
        map_urls=data.get("map_urls", {}),
    )

    return route