from typing import Dict, Any
from uuid import UUID

from ...domain.services.optimization_service import OptimizationService
from ...domain.repositories.route_repository import RouteRepository
from ...domain.exceptions.domain_exceptions import RouteNotFoundError


class OptimizeRouteCommand:
    """Command to optimize a route."""

    def __init__(self, route_repository=None, optimization_service=None):
        # These would typically be injected by a dependency injection container
        self.route_repository = route_repository or RouteRepository()
        self.optimization_service = optimization_service

    def execute(self, route_id: UUID, optimization_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Optimize a route using the provided parameters.

        Args:
            route_id: The ID of the route to optimize
            optimization_params: Parameters to customize the optimization

        Returns:
            Dict containing the optimization results
        """
        # Get the route from the repository
        route = self.route_repository.get_by_id(route_id)
        if not route:
            raise RouteNotFoundError(f"Route with ID {route_id} not found")

        # Optimize the route
        optimization_result = self.optimization_service.optimize_route(
            route=route,
            optimization_params=optimization_params
        )

        # Convert to DTO and return
        return {
            "id": str(optimization_result.id),
            "route_id": str(optimization_result.route_id),
            "optimized_waypoints": [
                {
                    "id": str(wp.id),
                    "name": wp.name,
                    "latitude": wp.latitude,
                    "longitude": wp.longitude,
                    "order": wp.order
                }
                for wp in optimization_result.optimized_waypoints
            ],
            "total_distance": optimization_result.total_distance,
            "total_duration": optimization_result.total_duration,
            "created_at": optimization_result.created_at.isoformat(),
            "optimization_params": optimization_result.optimization_params
        }
