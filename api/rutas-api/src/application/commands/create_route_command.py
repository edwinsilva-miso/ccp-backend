from typing import Dict, Any, List
from uuid import UUID

from ...domain.entities.route import Route
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
        validated_data = validate_route_dto(route_data)

        # Create waypoints
        waypoints = []
        for i, wp_data in enumerate(validated_data['waypoints']):
            waypoint = Waypoint(
                latitude=wp_data['latitude'],
                longitude=wp_data['longitude'],
                name=wp_data.get('name'),
                address=wp_data.get('address'),
                order=i
            )
            waypoints.append(waypoint)

        # Create the route
        route = self.route_service.create_route(
            name=validated_data['name'],
            description=validated_data.get('description'),
            waypoints=waypoints,
            user_id=validated_data.get('user_id')
        )

        # Return DTO
        return serialize_route(route)