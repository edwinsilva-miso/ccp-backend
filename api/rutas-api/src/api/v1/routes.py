from flask import Blueprint, request, jsonify, current_app
from uuid import UUID
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from ...application.commands.create_route_command import CreateRouteCommand
from ...application.commands.update_route_command import UpdateRouteCommand
from ...application.queries.get_route_query import GetRouteQuery
from ...domain.exceptions.domain_exceptions import RouteNotFoundError

routes_blueprint = Blueprint('routes', __name__)


@routes_blueprint.route('/routes', methods=['POST'])
def create_route():
    """Create a new route."""
    logger.debug("Received create route request")
    data = request.json
    logger.debug("Request data: %s", data)
    command = CreateRouteCommand(route_repository=current_app.route_repository)
    result = command.execute(data)
    return jsonify(result), 201


@routes_blueprint.route('/routes', methods=['GET'])
def list_routes():
    """List all routes."""
    logger.debug("Received list routes request")

    user_id = request.args.get('user_id')
    due_to = request.args.get('due_to')

    logger.debug("request parameters - user_id: %s, due_to: %s", user_id, due_to)

    if user_id:
        user_id = UUID(user_id)
        logger.debug("converted user_id to UUID: %s", user_id)

    logger.debug("initializing GetRouteQuery with route repository")
    query = GetRouteQuery(route_repository=current_app.route_repository)

    logger.debug("executing query to fetch routes")
    result = query.execute_list(user_id=user_id, due_to=due_to)

    logger.debug("query returned %d routes", len(result))
    logger.debug("preparing JSON response")
    return jsonify(result)


@routes_blueprint.route('/routes/<uuid:route_id>', methods=['GET'])
def get_route(route_id):
    """Get a route by ID."""
    logger.debug("Received get route request for ID: %s", route_id)
    try:
        query = GetRouteQuery(route_repository=current_app.route_repository)
        result = query.execute(route_id)
        return jsonify(result)
    except RouteNotFoundError:
        return jsonify({"error": f"Route with ID {route_id} not found"}), 404


@routes_blueprint.route('/routes/<uuid:route_id>', methods=['PUT'])
def update_route(route_id):
    """Update a route."""
    logger.debug("Received update route request for ID: %s", route_id)
    data = request.json
    logger.debug("Update data: %s", data)

    try:
        # Use the UpdateRouteCommand instead of CreateRouteCommand
        command = UpdateRouteCommand(route_repository=current_app.route_repository)
        result = command.execute(route_id, data)

        if result is None:
            return jsonify({"error": f"Route with ID {route_id} not found"}), 404

        return jsonify(result)
    except RouteNotFoundError:
        return jsonify({"error": f"Route with ID {route_id} not found"}), 404


@routes_blueprint.route('/routes/<uuid:route_id>', methods=['DELETE'])
def delete_route(route_id):
    """Delete a route."""
    logger.debug("Received delete route request for ID: %s", route_id)
    try:
        # Check if route exists
        query = GetRouteQuery(route_repository=current_app.route_repository)
        query.execute(route_id)

        # Delete the route
        current_app.route_repository.delete(route_id)

        return "", 204
    except RouteNotFoundError:
        return jsonify({"error": f"Route with ID {route_id} not found"}), 404
