import requests
from datetime import datetime, timezone
from typing import List

BASE_URL = "https://api.open-meteo.com/v1/forecast"


def _fetch_forecast(lat: float, lon: float) -> dict:
    """
    Fetch full forecast dataset from Open-Meteo.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,windspeed_10m,weathercode",
        "daily": "temperature_2m_max,temperature_2m_min,weathercode",
        "timezone": "UTC",
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def _closest_index(target: datetime, time_strings: List[str]) -> int:
    """
    Find index of forecast time closest to ETA.
    """
    times = [
        datetime.fromisoformat(t).replace(tzinfo=timezone.utc)
        for t in time_strings
    ]

    return min(
        range(len(times)),
        key=lambda i: abs((times[i] - target).total_seconds())
    )


def apply_weather_to_waypoint(waypoint) -> None:
    """
    Mutates Waypoint object with weather data.
    Requires:
        waypoint.lat
        waypoint.lon
        waypoint.eta (UTC datetime)
    """

    now = datetime.now(timezone.utc)  # aware datetime in UTC
    seconds_ahead = (waypoint.eta.astimezone(timezone.utc) - now).total_seconds()

    if seconds_ahead < 0:
        waypoint.weather_source = "past"
        return

    if seconds_ahead > 14 * 86400:
        waypoint.weather_source = "out_of_range"
        return

    data = _fetch_forecast(waypoint.lat, waypoint.lon)

    # ≤ 5 days → hourly
    if seconds_ahead <= 5 * 86400:
        idx = _closest_index(
            waypoint.eta,
            data["hourly"]["time"]
        )

        waypoint.weather_source = "hourly"
        waypoint.forecast_time = datetime.fromisoformat(
            data["hourly"]["time"][idx]
        ).replace(tzinfo=timezone.utc)

        waypoint.temperature_c = data["hourly"]["temperature_2m"][idx]
        waypoint.wind_speed_ms = data["hourly"]["windspeed_10m"][idx]
        waypoint.weather_code = data["hourly"]["weathercode"][idx]

        return

    # > 5 days → daily
    idx = _closest_index(
        waypoint.eta,
        data["daily"]["time"]
    )

    waypoint.weather_source = "daily"
    waypoint.forecast_time = datetime.fromisoformat(
        data["daily"]["time"][idx]
    ).replace(tzinfo=timezone.utc)

    waypoint.temp_min_c = data["daily"]["temperature_2m_min"][idx]
    waypoint.temp_max_c = data["daily"]["temperature_2m_max"][idx]
    waypoint.weather_code = data["daily"]["weathercode"][idx]