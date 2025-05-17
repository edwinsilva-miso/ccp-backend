from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from .waypoint import Waypoint


@dataclass
class Route:
    """Route entity representing a collection of waypoints."""
    name: str
    waypoints: List[Waypoint]
    description: Optional[str] = None
    user_id: Optional[UUID] = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    zone: Optional[str] = None
    due_to: datetime = field(default_factory=datetime.utcnow)

    def add_waypoint(self, waypoint: Waypoint) -> None:
        """Add a waypoint to the route."""
        self.waypoints.append(waypoint)
        self.updated_at = datetime.utcnow()

    def remove_waypoint(self, waypoint_id: UUID) -> None:
        """Remove a waypoint from the route."""
        self.waypoints = [wp for wp in self.waypoints if wp.id != waypoint_id]
        self.updated_at = datetime.utcnow()

    def reorder_waypoints(self, new_order: List[UUID]) -> None:
        """Reorder the waypoints based on the provided list of IDs."""
        # Create a mapping of waypoint IDs to waypoints
        waypoint_map = {wp.id: wp for wp in self.waypoints}

        # Validate that all IDs are present
        if set(new_order) != set(waypoint_map.keys()):
            raise ValueError("The list of IDs does not match the waypoints in the route")

        # Reorder waypoints
        self.waypoints = [waypoint_map[wp_id] for wp_id in new_order]

        # Update order property
        for i, waypoint in enumerate(self.waypoints):
            waypoint.order = i

        self.updated_at = datetime.utcnow()
