import logging
from datetime import datetime

from flask import Blueprint, request

from ..adapters.routes_adapter import RoutesAdapter
from ..utils.commons import validate_token

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

routes_blueprint = Blueprint('routes', __name__, url_prefix='/bff/v1/mobile/routes')


@routes_blueprint.route('', methods=['POST'])
@validate_token
def create_route(jwt):
    logger.debug("received request to create a new route")

    route_data = request.get_json()

    adapter = RoutesAdapter()
    return adapter.create_route(jwt, route_data)


@routes_blueprint.route('/<uuid:route_id>', methods=['GET'])
@validate_token
def get_route(route_id, jwt):
    """Get a route by ID."""
    logger.debug(f"received request to get route with id: {route_id}")
    adapter = RoutesAdapter()
    return adapter.get_route_by_id(jwt, route_id)


@routes_blueprint.route('/<uuid:route_id>', methods=['PUT'])
@validate_token
def update_route(route_id, jwt):
    """Update a route."""
    logger.debug(f"received request to update route with id: {route_id}")
    route_data = request.get_json()
    adapter = RoutesAdapter()
    return adapter.update_route_by_id(jwt, route_id, route_data)


@routes_blueprint.route('/<uuid:route_id>', methods=['DELETE'])
@validate_token
def delete_route(route_id, jwt):
    """Delete a route."""
    logger.debug(f"received request to delete route with id: {route_id}")
    adapter = RoutesAdapter()
    return adapter.delete_route_by_id(jwt, route_id)


@routes_blueprint.route('/users/<user_id>', methods=['GET'])
@validate_token
def get_user_routes(user_id, jwt):
    logger.debug(f"received request to get product with id: {user_id}")
    logger.debug("retrieving product by id from bff web.")

    raw_date = request.args.get('due_to')
    try:
        # Parse from ISO 8601 format
        parsed_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        parsed_date = None

    adapter = RoutesAdapter()
    return adapter.get_user_routes_by_date(jwt, user_id, parsed_date)
