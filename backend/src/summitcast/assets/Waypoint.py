from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple, List, Dict

@dataclass
class Waypoint:
    title: str
    lat: float
    lon: float
    distance_into_route: float = 0
    elevation: Optional[float] = 0
    categories: List[str] = None
    eta: Optional[datetime] = None
    # Weather fields
    weather_source: Optional[str] = None  # "hourly" or "daily"
    forecast_time: Optional[datetime] = None
    temperature_c: Optional[float] = None
    temp_min_c: Optional[float] = None
    temp_max_c: Optional[float] = None
    wind_speed_ms: Optional[float] = None
    weather_code: Optional[int] = None