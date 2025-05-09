from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

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
        if not route_id or not isinstance(route_id, UUID):
            raise ValueError("Invalid route ID, not a valid UUID or empty")

        route = self.route_service.get_route(route_id)
        return serialize_route(route)

    def execute_list(self, user_id: Optional[UUID] = None, due_to: str = None) -> List[Dict[str, Any]]:
        """
        Get all routes, optionally filtered by user ID.

        Args:
            user_id: Optional user ID to filter routes
            due_to: Optional due date to filter routes by, in datetime.date format

        Returns:
            List of dictionaries, representing routes
        """
        logger.debug("executing get_routes with user_id: %s and due_to: %s", user_id, due_to)
        routes = self.route_service.get_routes(user_id)
        logger.debug("retrieved %d routes from service", len(routes))
        routes_ = []

        try:
            for route in routes:
                if due_to:
                    exact_date = datetime.strptime(due_to, "%Y-%m-%d").date()

                    logger.debug("filtering route %s by due date %s", route.id, due_to)
                    if route.due_to and route.due_to.date() == exact_date:
                        logger.debug("route %s matches due date criteria", route.id)
                        routes_.append(serialize_route(route))
                else:
                    routes_.append(serialize_route(route))
        except Exception as e:
            logger.error("Error creating route: %s", e.__traceback__)
            logger.debug("Exception stack trace:", exc_info=True)
            raise

        logger.debug("returning %d filtered routes", len(routes_))
        return routes_
