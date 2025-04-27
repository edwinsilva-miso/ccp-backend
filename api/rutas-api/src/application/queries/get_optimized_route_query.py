from typing import Dict, Any
from uuid import UUID

from ...domain.repositories.route_repository import RouteRepository
from ...domain.services.optimization_service import OptimizationService
from ...domain.entities.optimization_result import OptimizationResult


class GetOptimizedRouteQuery:
    """Query to get an optimized route."""

    def __init__(self, route_repository=None, optimization_service=None):
        # These would typically be injected
        self.route_repository = route_repository or RouteRepository()
        self.optimization_service = optimization_service or OptimizationService()

    def execute(self, optimization_result: OptimizationResult) -> Dict[str, Any]:
        """
        Get the details of an optimized route.

        Args:
            optimization_result: The optimization result entity

        Returns:
            Dictionary representation of the optimization result
        """
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
