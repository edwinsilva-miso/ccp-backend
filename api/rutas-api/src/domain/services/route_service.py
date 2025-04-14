from typing import List, Optional
from uuid import UUID

from ..entities.route import Route
from ..entities.waypoint import Waypoint
from ..repositories.route_repository import RouteRepository
from ..exceptions.domain_exceptions import RouteNotFoundError


class RouteService:
    """Service for route operations."""

    def __init__(self, route_repository: RouteRepository):
        self.route_repository = route_repository

    def create_route(self, name: str, description: Optional[str] = None,
                     waypoints: Optional[List[Waypoint]] = None,
                     user_id: Optional[UUID] = None) -> Route:
        """Create a new route."""
        route = Route(
            name=name,
            description=description,
            waypoints=waypoints or [],
            user_id=user_id
        )
        return self.route_repository.create(route)

    def get_route(self, route_id: UUID) -> Route:
        """Get a route by ID."""
        route = self.route_repository.get_by_id(route_id)
        if not route:
            raise RouteNotFoundError(f"Route with ID {route_id} not found")
        return route

    def get_routes(self, user_id: Optional[UUID] = None) -> List[Route]:
        """Get all routes, optionally filtered by user ID."""
        return self.route_repository.get_all(user_id)

    def update_route(self, route_id: UUID, updates: dict) -> Route:
        """Update a route."""
        route = self.get_route(route_id)

        # Apply updates
        if 'name' in updates:
            route.name = updates['name']
        if 'description' in updates:
            route.description = updates['description']

        # Handle waypoints updates if present
        if 'waypoints' in updates:
            # Create new waypoints
            waypoints = []
            for i, wp_data in enumerate(updates['waypoints']):
                waypoint = Waypoint(
                    latitude=wp_data['latitude'],
                    longitude=wp_data['longitude'],
                    name=wp_data.get('name'),
                    address=wp_data.get('address'),
                    order=i
                )
                waypoints.append(waypoint)
            route.waypoints = waypoints

        return self.route_repository.update(route)

    def delete_route(self, route_id: UUID) -> None:
        """Delete a route."""
        # Check if the route exists
        self.get_route(route_id)
        # Delete the route
        self.route_repository.delete(route_id)
