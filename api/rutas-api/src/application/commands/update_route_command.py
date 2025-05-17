from typing import Dict, Any, Optional
from uuid import UUID

from ...domain.repositories.route_repository import RouteRepository
from ...domain.services.route_service import RouteService
from ...domain.exceptions.domain_exceptions import RouteNotFoundError
from ...application.dtos.route_dto import validate_route_dto, serialize_route


class UpdateRouteCommand:
    """Command to update an existing route."""

    def __init__(self, route_repository=None):
        # This would typically be injected
        self.route_repository = route_repository or RouteRepository()
        self.route_service = RouteService(self.route_repository)

    def execute(self, route_id: UUID, route_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing route with the provided data.

        Args:
            route_id: UUID of the route to update
            route_data: Dictionary containing updated route data

        Returns:
            Dictionary representation of the updated route or None if route not found
        """
        # Validate the data
        validated_data = validate_route_dto(route_data)

        try:
            # Update the route using the service
            # Pass the validated data directly to update_route which expects a dictionary
            updated_route = self.route_service.update_route(
                route_id=route_id,
                updates=validated_data
            )

            # Return DTO
            return serialize_route(updated_route)
        except RouteNotFoundError:
            return None
