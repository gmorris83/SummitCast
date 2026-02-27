
from typing import Dict, Any

from strava.domains import Athlete, Waypoint, Segment, Route


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
            elevation= None,
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
