from flask import Blueprint, request, jsonify, current_app
from uuid import UUID

from ...application.queries.get_route_query import GetRouteQuery
from ...application.queries.get_optimized_route_query import GetOptimizedRouteQuery
from ...domain.exceptions.domain_exceptions import RouteNotFoundError, OptimizationError

optimizations_blueprint = Blueprint('optimizations', __name__)


@optimizations_blueprint.route('/routes/<uuid:route_id>/optimize', methods=['POST'])
def optimize_route(route_id):
    """Optimize a route."""
    try:
        # Get optimization parameters
        params = request.json or {}

        # Get the route
        route_query = GetRouteQuery(route_repository=current_app.route_repository)
        route_data = route_query.execute(route_id)

        # Convert route_data back to domain entity (this is a bit of a hack, but works for demo)
        from ...domain.entities.route import Route
        from ...domain.entities.waypoint import Waypoint

        waypoints = [
            Waypoint(
                id=UUID(wp['id']),
                latitude=wp['latitude'],
                longitude=wp['longitude'],
                name=wp.get('name'),
                address=wp.get('address'),
                order=wp.get('order')
            )
            for wp in route_data['waypoints']
        ]

        route = Route(
            id=UUID(route_data['id']),
            name=route_data['name'],
            description=route_data.get('description'),
            user_id=UUID(route_data['user_id']) if route_data.get('user_id') else None,
            waypoints=waypoints
        )

        # Optimize the route
        optimization_result = current_app.optimization_service.optimize_route(
            route=route,
            optimization_params=params
        )

        # Return the result
        optimization_query = GetOptimizedRouteQuery()
        result = optimization_query.execute(optimization_result)

        return jsonify(result)
    except RouteNotFoundError:
        return jsonify({"error": f"Route with ID {route_id} not found"}), 404
    except OptimizationError as e:
        return jsonify({"error": str(e)}), 400
