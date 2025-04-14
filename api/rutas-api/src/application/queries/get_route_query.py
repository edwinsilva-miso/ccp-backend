from typing import Dict, Any, List, Optional
from uuid import UUID

from ...domain.services.route_service import RouteService
from ...domain.repositories.route_repository import RouteRepository
from ..dtos.route_dto import serialize_route


class GetRouteQuery:
    """Query to get route(s)."""

    def __init__(self, route_repository=None):
        # This would typically be injected
        self.route_repository = route_repository or RouteRepository()
        self.route_service = RouteService(self.route_repository)

    def execute(self, route_id: UUID) -> Dict[str, Any]:
        """
        Get a route by ID.

        Args:
            route_id: ID of the route to get

        Returns:
            Dictionary representation of the route
        """
        route = self.route_service.get_route(route_id)
        return serialize_route(route)

    def execute_list(self, user_id: Optional[UUID] = None) -> List[Dict[str, Any]]:
        """
        Get all routes, optionally filtered by user ID.

        Args:
            user_id: Optional user ID to filter routes

        Returns:
            List of dictionary representations of routes
        """
        routes = self.route_service.get_routes(user_id)
        return [serialize_route(route) for route in routes]
