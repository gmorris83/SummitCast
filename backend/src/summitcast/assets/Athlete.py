from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple, List, Dict


@dataclass
class Athlete:
    id: int
    username: str
    firstname: str
    lastname: str
    city: Optional[str]
    country: Optional[str]
    weight: Optional[float]