from typing import Any, Dict

import requests
import polyline
from weather.weather import apply_weather_to_waypoint
from datetime import datetime, timedelta, timezone
from .parser import parse_strava_route
from .strava_tokens import get_valid_access_token
from .domains import Athlete,Waypoint,Segment,Route
from weather.weather_codes import WeatherCode

ROUTE_ID = '3406267604191386846'
#https://www.strava.com/routes/3360377804620477768

# The Lunar Round
#https://www.strava.com/routes/3406267604191386846

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

def get_route(route_id):
    url = f"https://www.strava.com/api/v3/routes/{route_id}"
    tokens = get_valid_access_token()
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()

def get_route_from_file():
    try:
        with open('../lunar_round.json', 'r') as file:
            return file.read()
    except FileNotFoundError:
        print('File not found')
    return

def get_route_points(data):
    encoded = data.polyline
    #print(f'Encoded Route:\n{encoded}')
    # Decode into list of (lat, lng)
    points = polyline.decode(encoded)
    #print(f'Decoded Route:\n{points}')
    return points

def print_info(route):
    print("--------------------------------------------------")
    print(route.name)
    average_pace_mins = 12.03
    time = total_time(route.distance, average_pace_mins)
    formatted_time = format_timedelta(time)

    print(f'Expected completion time: {formatted_time} based on Avg Pace: {average_pace_mins} min/km')
    print(f'Created By: {route.athlete.firstname} {route.athlete.lastname}')
    print('Distance: ' + "{:.2f} km".format(route.distance / 1000))
    print('Elevation: ' + "{:.2f} meters".format(route.elevation_gain))
    print(f'Number of Marked Summits: {len(route.waypoints)}')
    print("--------------------------------------------------")

def get_elevations(points):
    print(f'Getting elevation data for {len(points)} Summits')
    locations = "|".join([f"{lat},{lng}" for lat, lng in points])

    url = f"https://api.opentopodata.org/v1/srtm90m?locations={locations}"

    response = requests.get(url)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    results = response.json()["results"]

    data = response.json()

    return [
        {"lat": p[0], "lng": p[1], "elev": r["elevation"]}
        for p, r in zip(points, results)
    ]

def get_waypoint_elevations(route):
    """
    waypoints: list of dicts with 'latlng': [lat, lng]
    returns: list of dicts with lat, lng, elevation
    """
    results = []
    for wp in route.waypoints:
        url = f"https://api.opentopodata.org/v1/srtm90m?locations={wp.lat},{wp.lon}"
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        elev = data["results"][0]["elevation"]  # single point
        wp.elevation = elev
        for wp in route.waypoints:
            print(f'Waypoint: {wp.title} Elevation: {elev}\n')

def calculate_etas(route, start_time: datetime, avg_speed_kmh: float):
    """Assign ETA based on distance_into_route and average speed."""
    print(f'Start Time: {start_time} : Avg Speed: {avg_speed_kmh} kmh')
    for index, wp in enumerate(route.waypoints):
        hours = (wp.distance_into_route / 1000) / avg_speed_kmh
        wp.eta = start_time + timedelta(hours=hours)
        if index == 0:
            print(f'{wp.title}: {wp.eta}')
        else:
            print(f'{wp.title}: ETA: {wp.eta}')

def format_timedelta(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def total_time(distance_meters: float, pace_min_per_km: float) -> timedelta:
    """
    distance_meters: total route distance in meters
    pace_min_per_km: average pace in minutes per km
    returns: timedelta representing total time
    """
    distance_km = distance_meters / 1000
    total_minutes = distance_km * pace_min_per_km
    return timedelta(minutes=total_minutes)

def get_weather_for_route(route):
    print("Applying Weather")
    for wp in route.waypoints:
        apply_weather_to_waypoint(wp)
        temp = wp.temperature_c
        print(f'Waypoint: {wp.title} Weather:{WeatherCode.text(wp.weather_code)} '
              f'Temp:{temp} Wind Speed:{wp.wind_speed_ms}')


def main():
    print("Starting Strava Parser...")
    #ROUTE_ID = input('Enter Strava Route ID:\n')
    strava_route = get_route(ROUTE_ID)
    route = parse_strava_route(strava_route)
    rp = get_route_points(route)
    start_RP = rp[0]
    end_RP = rp[len(rp) - 1]
    route.waypoints.insert(0, Waypoint(title="Start", lat=start_RP[0], lon=start_RP[1], distance_into_route=0))
    route.waypoints.append(Waypoint(title="Finish", lat=end_RP[0], lon=end_RP[1], distance_into_route=route.distance))
    print_info(route)
    # elevation_data = get_waypoint_elevations(route)
    # get eta at each point
    start_utc = datetime.now(timezone.utc) + timedelta(days=2)

    calculate_etas(route, start_time=start_utc, avg_speed_kmh=10)
    get_weather_for_route(route)
    print("Strava Parser Completed.")

main()
