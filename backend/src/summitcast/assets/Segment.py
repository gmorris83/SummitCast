from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple, List, Dict


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