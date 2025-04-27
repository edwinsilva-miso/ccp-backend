import logging

from typing import List, Optional
from uuid import UUID

from ..entities.route import Route
from ..entities.waypoint import Waypoint
from ..repositories.route_repository import RouteRepository
from ..exceptions.domain_exceptions import RouteNotFoundError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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
        """
        Update a route with the provided updates.

        Args:
            route_id: UUID of the route to update
            updates: Dictionary containing updated route data

        Returns:
            Updated Route entity

        Raises:
            RouteNotFoundError: If the route doesn't exist
        """
        # Check if route exists, this will raise RouteNotFoundError if not found
        self.get_route(route_id)

        # The repository.update method can either take a Route object or a dictionary
        # We're passing the updates dictionary directly, which is more efficient
        # as it avoids first constructing a Route object
        updated_route = None
        try:
            updated_route = self.route_repository.update(route_id, updates)
        except Exception as e:
            logger.error("Error updating route: %s", e.__traceback__)
            logger.debug("Exception stack trace:", exc_info=True)

        if not updated_route:
            raise RouteNotFoundError(f"Route with ID {route_id} not found after update")

        return updated_route

    def delete_route(self, route_id: UUID) -> None:
        """Delete a route."""
        # Check if the route exists
        self.get_route(route_id)
        # Delete the route
        self.route_repository.delete(route_id)
