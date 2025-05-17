from typing import Dict, Any, List
from uuid import UUID
import json
import logging

from ...domain.entities.route import Route
from ...domain.exceptions.domain_exceptions import InvalidRouteError, InvalidWaypointError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def validate_route_dto(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate route data from API request.

    Args:
        data: Dictionary containing route data

    Returns:
        Validated data dictionary

    Raises:
        InvalidRouteError: If route data is invalid
        InvalidWaypointError: If waypoint data is invalid
    """
    logger.debug("starting route validation")
    logger.debug(f"validating data type: {type(data)}")
    if not isinstance(data, dict):
        logger.debug(f"invalid data type, expected dict, got: {type(data)}")
        raise InvalidRouteError("Invalid route datatype. Must be a dictionary")

    # Validate required fields
    logger.debug("validating required fields")
    if 'name' not in data:
        logger.debug("name field is missing")
        raise InvalidRouteError("Route name is required")

    logger.debug("validating name field type and content")
    if not isinstance(data['name'], str) or not data['name'].strip():
        logger.debug(f"invalid name field: {data.get('name')}")
        raise InvalidRouteError("Route name must be a non-empty string")

    # Validate waypoints
    logger.debug("validating waypoints")
    waypoints = data.get('waypoints', [])
    if not isinstance(waypoints, list):
        logger.debug("invalid waypoints type, expected list, got: %s", type(waypoints))
        raise InvalidRouteError("Waypoints must be a list")

    validated_waypoints = []
    for i, waypoint in enumerate(waypoints):
        logger.debug(f"validating waypoint at index {i}")
        if not isinstance(waypoint, dict):
            logger.debug(f"invalid waypoint type at index {i}, expected dict, got: {type(waypoint)}")
            raise InvalidWaypointError(f"Waypoint at index {i} must be an object")

        # Validate required waypoint fields
        logger.debug("checking required waypoint fields at index %d", i)
        if 'latitude' not in waypoint:
            logger.debug("missing latitude in waypoint at index %d", i)
            raise InvalidWaypointError(f"Waypoint at index {i} is missing latitude")

        if 'longitude' not in waypoint:
            logger.debug("missing longitude in waypoint at index %d", i)
            raise InvalidWaypointError(f"Waypoint at index {i} is missing longitude")

        try:
            logger.debug("converting coordinates to float at index %d", i)
            latitude = float(waypoint['latitude'])
            longitude = float(waypoint['longitude'])
        except (ValueError, TypeError):
            logger.debug(
                f"invalid coordinate values at index {i}: lat={waypoint['latitude']}, lon={waypoint['longitude']}")
            raise InvalidWaypointError(f"Waypoint at index {i} has invalid coordinates")

        # Validate latitude and longitude ranges
        logger.debug(f"validating coordinate ranges at index {i}: lat={latitude}, lon={longitude}")
        if not (-90 <= latitude <= 90):
            logger.debug(f"invalid latitude at index {i}: {latitude}")
            raise InvalidWaypointError(f"Waypoint at index {i} has invalid latitude (must be between -90 and 90)")

        if not (-180 <= longitude <= 180):
            logger.debug(f"invalid longitude at index {i}: {longitude}")
            raise InvalidWaypointError(f"Waypoint at index {i} has invalid longitude (must be between -180 and 180)")

        # Create validated waypoint
        logger.debug(f"creating validated waypoint for index {i}")
        validated_waypoint = {
            'latitude': latitude,
            'longitude': longitude,
            'name': waypoint.get('name'),
            'address': waypoint.get('address'),
            'order': i
        }

        validated_waypoints.append(validated_waypoint)

    # Create validated data
    validated_data = {
        'name': data['name'],
        'description': data.get('description'),
        'zone': data.get('zone'),
        'due_to': data.get('due_to'),
        'waypoints': validated_waypoints,
    }

    # Add user_id if present
    logger.debug("checking for user_id in data")
    if 'user_id' in data and data['user_id']:
        try:
            logger.debug(f"validating user_id: {data['user_id']}")
            user_id = UUID(data['user_id']) if isinstance(data['user_id'], str) else data['user_id']
            validated_data['user_id'] = user_id
        except (ValueError, TypeError, AttributeError):
            raise InvalidRouteError("Invalid user_id")

    logger.debug(f"route validation completed successfully with data: {validated_data}")
    return validated_data


def serialize_route(route: Route) -> Dict[str, Any]:
    """
    Serialize a route entity to a dictionary.

    Args:
        route: Route entity to serialize

    Returns:
        Dictionary representation of the route
    """
    return {
        'id': str(route.id),
        'name': route.name,
        'description': route.description,
        'user_id': str(route.user_id) if route.user_id else None,
        'created_at': route.created_at.isoformat(),
        'updated_at': route.updated_at.isoformat(),
        'zone': route.zone,
        'due_to': route.due_to.isoformat(),
        'waypoints': [
            {
                'id': str(wp.id),
                'name': wp.name,
                'latitude': wp.latitude,
                'longitude': wp.longitude,
                'address': wp.address,
                'order': wp.order,
                'created_at': wp.created_at.isoformat()
            }
            for wp in route.waypoints
        ]
    }
