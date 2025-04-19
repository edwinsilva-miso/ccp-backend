from flask import jsonify

from ..domain.exceptions.domain_exceptions import (
    DomainError,
    RouteNotFoundError,
    OptimizationError,
    InvalidRouteError,
    InvalidWaypointError
)


def register_error_handlers(app):
    """Register error handlers for the application."""

    @app.errorhandler(RouteNotFoundError)
    def handle_route_not_found(error):
        return jsonify({"error": str(error)}), 404

    @app.errorhandler(OptimizationError)
    def handle_optimization_error(error):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(InvalidRouteError)
    def handle_invalid_route(error):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(InvalidWaypointError)
    def handle_invalid_waypoint(error):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(DomainError)
    def handle_domain_error(error):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(Exception)
    def handle_general_exception(error):
        # Log the error here
        return jsonify({"error": "An unexpected error occurred"}), 500

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({"error": "Method not allowed"}), 405
