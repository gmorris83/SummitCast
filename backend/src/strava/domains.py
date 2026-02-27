from dataclasses import dataclass

@dataclass
class Athlete:
    id: int
    username: str
    firstname: str
    lastname: str
    city: Optional[str]
    country: Optional[str]
    weight: Optional[float]


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


@dataclass
class Segment:
    id: int
    name: str
    distance: float
    average_grade: float
    max_grade: float
    elevation_high: float
    elevation_low: float
    start_latlng: Tuple[float, float]
    end_latlng: Tuple[float, float]


@dataclass
class Route:
    id: int
    name: str
    description: str
    distance: float
    elevation_gain: float
    estimated_moving_time: int
    polyline: str
    athlete: Athlete
    waypoints: List[Waypoint]
    segments: List[Segment]
    map_urls: Dict[str, str]