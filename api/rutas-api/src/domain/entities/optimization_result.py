from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional
from uuid import UUID, uuid4

from .waypoint import Waypoint


@dataclass
class OptimizationResult:
    """Entity representing the result of a route optimization."""
    route_id: UUID
    optimized_waypoints: List[Waypoint]
    total_distance: float  # in meters
    total_duration: float  # in seconds
    optimization_params: Optional[Dict[str, Any]] = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
