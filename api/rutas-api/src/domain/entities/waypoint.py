from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Waypoint:
    """Waypoint entity representing a location on a route."""
    latitude: float
    longitude: float
    name: Optional[str] = None
    address: Optional[str] = None
    order: Optional[int] = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def coordinates(self) -> tuple[float, float]:
        """Return the coordinates as a tuple (longitude, latitude)."""
        return (self.longitude, self.latitude)
