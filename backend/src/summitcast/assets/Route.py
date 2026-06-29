from dataclasses import dataclass, field
from typing import List, Dict
from .Athlete import Athlete
from .Waypoint import Waypoint
from .Segment import Segment

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
    distance_profile: List[float] = field(default_factory=list)
    elevation_profile: List[float] = field(default_factory=list)

    @property
    def distance_meters(self) -> float:
        """Return distance in meters (rounded to 2 decimal places)."""
        return round(self.distance, 2)

    @property
    def distance_km(self) -> float:
        """Return distance in kilometers (rounded to 2 decimal places)."""
        return round(self.distance / 1000, 2)

    @property
    def distance_miles(self) -> float:
        """Return distance in miles (rounded to 2 decimal places)."""
        return round(self.distance / 1609.344, 2)