from typing import Dict, Any, List
from uuid import UUID
import json

from ...domain.entities.route import Route
from ...domain.exceptions.domain_exceptions import InvalidRouteError, InvalidWaypointError


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
    if not isinstance(data, dict):
        raise InvalidRouteError("Invalid route datatype. Must be a dictionary")

    # Validate required fields
    if 'name' not in data:
        raise InvalidRouteError("Route name is required")

    if not isinstance(data['name'], str) or not data['name'].strip():
        raise InvalidRouteError("Route name must be a non-empty string")

    # Validate waypoints
    waypoints = data.get('waypoints', [])
    if not isinstance(waypoints, list):
        raise InvalidRouteError("Waypoints must be a list")

    validated_waypoints = []
    for i, waypoint in enumerate(waypoints):
        if not isinstance(waypoint, dict):
            raise InvalidWaypointError(f"Waypoint at index {i} must be an object")

        # Validate required waypoint fields
        if 'latitude' not in waypoint:
            raise InvalidWaypointError(f"Waypoint at index {i} is missing latitude")

        if 'longitude' not in waypoint:
            raise InvalidWaypointError(f"Waypoint at index {i} is missing longitude")

        try:
            latitude = float(waypoint['latitude'])
            longitude = float(waypoint['longitude'])
        except (ValueError, TypeError):
            raise InvalidWaypointError(f"Waypoint at index {i} has invalid coordinates")

        # Validate latitude and longitude ranges
        if not (-90 <= latitude <= 90):
            raise InvalidWaypointError(f"Waypoint at index {i} has invalid latitude (must be between -90 and 90)")

        if not (-180 <= longitude <= 180):
            raise InvalidWaypointError(f"Waypoint at index {i} has invalid longitude (must be between -180 and 180)")

        # Create validated waypoint
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
        'waypoints': validated_waypoints,
    }

    # Add user_id if present
    if 'user_id' in data and data['user_id']:
        try:
            user_id = UUID(data['user_id']) if isinstance(data['user_id'], str) else data['user_id']
            validated_data['user_id'] = user_id
        except (ValueError, TypeError, AttributeError):
            raise InvalidRouteError("Invalid user_id")

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
