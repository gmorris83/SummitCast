from typing import Dict, Any

import polyline
import requests

from summitcast.assets.Athlete import Athlete
from summitcast.assets.Route import Route
from summitcast.assets.Waypoint import Waypoint
from summitcast.assets.Segment import Segment
from summitcast.helpers import strava_tokens

#https://www.strava.com/routes/3406267604191386846


class StravaService:
    def __init__(self, strava_route_id: str):
        self.route_id = strava_route_id

    def get_strava_route_id(self):
        return self.route_id

    @staticmethod
    def decode_polyline(route: Route):
        decoded_route = polyline.decode(route.polyline)
        return decoded_route

    def get_strava_route(self):
        if not self.route_id:
            raise Exception("Error: Route ID is required to fetch Strava route data.")

        print(f"Fetching Strava route from URL: {self.route_id}")
        url = f"https://www.strava.com/api/v3/routes/{self.route_id}"
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
        return self.parse_strava_route(data)


    def parse_strava_route(self, data: Dict[str, Any]) -> Route:
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

        map_data = data.get("map", {})
        polyline = (
            map_data.get("polyline")
            or map_data.get("summary_polyline")
        )

        route = Route(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            distance= data["distance"],
            elevation_gain=data["elevation_gain"],
            estimated_moving_time=data["estimated_moving_time"],
            polyline=data["map"]["polyline"],
            athlete=athlete,
            waypoints=waypoints,
            segments=segments,
            map_urls=data.get("map_urls", {}),
        )
        ## Decode the polyline into list of (lat, lng) pairs
        route.polyline = self.decode_polyline(route)
        return route