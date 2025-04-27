from typing import Dict, Any, List, Optional
from uuid import UUID

from ..entities.route import Route
from ..entities.waypoint import Waypoint
from ..entities.optimization_result import OptimizationResult
from ..exceptions.domain_exceptions import OptimizationError


class OptimizationService:
    """Service for route optimization."""

    def __init__(self, openroute_client):
        self.openroute_client = openroute_client

    def optimize_route(self, route: Route, optimization_params: Optional[Dict[str, Any]] = None) -> OptimizationResult:
        """
        Optimize a route using the OpenRoute Service.

        Args:
            route: The route to optimize
            optimization_params: Parameters to customize the optimization

        Returns:
            An OptimizationResult containing the optimized route
        """
        if not route.waypoints or len(route.waypoints) < 2:
            raise OptimizationError("Route must have at least 2 waypoints to optimize")

        # Use default params if none provided
        params = optimization_params or {}

        try:
            # Call the OpenRoute Service
            optimization_result = self.openroute_client.optimize_route(
                waypoints=[wp.coordinates for wp in route.waypoints],
                params=params
            )

            # Process the result
            optimized_waypoint_indices = optimization_result.get('waypoint_order', [])

            # Get the original waypoints in the optimized order
            optimized_waypoints = []
            for i, idx in enumerate(optimized_waypoint_indices):
                waypoint = route.waypoints[idx]
                # Create a new waypoint with the updated order
                new_waypoint = Waypoint(
                    latitude=waypoint.latitude,
                    longitude=waypoint.longitude,
                    name=waypoint.name,
                    address=waypoint.address,
                    order=i
                )
                optimized_waypoints.append(new_waypoint)

            # Get distance and duration
            total_distance = sum(leg.get('distance', 0) for leg in optimization_result.get('legs', []))
            total_duration = sum(leg.get('duration', 0) for leg in optimization_result.get('legs', []))

            # Create and return the optimization result
            return OptimizationResult(
                route_id=route.id,
                optimized_waypoints=optimized_waypoints,
                total_distance=total_distance,
                total_duration=total_duration,
                optimization_params=params
            )

        except Exception as e:
            raise OptimizationError(f"Error optimizing route: {str(e)}")
