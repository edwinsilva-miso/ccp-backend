import logging
from typing import Dict, Any, List
from uuid import UUID

from ...domain.entities.route import Route

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
from ...domain.entities.waypoint import Waypoint
from ...domain.services.route_service import RouteService
from ...domain.repositories.route_repository import RouteRepository
from ...infrastructure.repositories.sqlalchemy_route_repository import SQLAlchemyRouteRepository
from ..dtos.route_dto import validate_route_dto, serialize_route


class CreateRouteCommand:
    """Command to create a new route."""

    def __init__(self, route_repository=None):
        # This would typically be injected
        self.route_repository = route_repository or RouteRepository()
        self.route_service = RouteService(self.route_repository)

    def execute(self, route_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new route from the provided data.

        Args:
            route_data: Dictionary containing route data

        Returns:
            Dictionary representation of the created route
        """
        # Validate the data
        logger.debug("validating route data: %s", route_data)
        validated_data = validate_route_dto(route_data)
        logger.debug("route data validation successful")

        # Create waypoints
        logger.debug("creating waypoints from validated data")
        waypoints = []
        for i, wp_data in enumerate(validated_data['waypoints']):
            logger.debug("creating waypoint %d: %s", i, wp_data)
            waypoint = Waypoint(
                latitude=wp_data['latitude'],
                longitude=wp_data['longitude'],
                name=wp_data.get('name'),
                address=wp_data.get('address'),
                order=i
            )
            waypoints.append(waypoint)

        # Create the route
        logger.debug("creating new route with name: %s", validated_data['name'])
        route = self.route_service.create_route(
            Route(
                name=validated_data['name'],
                description=validated_data.get('description'),
                zone=validated_data.get('zone'),
                due_to=validated_data.get('due_to'),
                waypoints=waypoints,
                user_id=validated_data.get('user_id')
            )
        )

        # Return DTO
        logger.debug("serializing created route with id: %s", route.id)
        return serialize_route(route)
