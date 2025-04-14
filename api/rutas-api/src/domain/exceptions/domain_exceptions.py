class DomainError(Exception):
    """Base class for domain exceptions."""
    pass


class RouteNotFoundError(DomainError):
    """Raised when a route is not found."""
    pass


class OptimizationError(DomainError):
    """Raised when there's an error during route optimization."""
    pass


class InvalidRouteError(DomainError):
    """Raised when a route is invalid."""
    pass


class InvalidWaypointError(DomainError):
    """Raised when a waypoint is invalid."""
    pass
