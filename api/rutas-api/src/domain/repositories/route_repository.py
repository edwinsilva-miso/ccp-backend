from abc import ABC, abstractmethod
from typing import List, Optional, Union
from uuid import UUID

from src.domain.models.route import Route


class RouteRepository(ABC):
    """
    Abstract interface for Route repository operations.
    This defines the contract that concrete implementations must follow.
    """

    @abstractmethod
    def create(self, route: Route) -> Route:
        """
        Create a new route.

        Args:
            route: The route to create

        Returns:
            The created route with assigned ID
        """
        pass

    @abstractmethod
    def get_by_id(self, route_id: UUID) -> Optional[Route]:
        """
        Get a route by its ID.

        Args:
            route_id: The ID of the route to retrieve

        Returns:
            The route if found, None otherwise
        """
        pass

    @abstractmethod
    def get_all(self, user_id: Optional[UUID] = None) -> List[Route]:
        """
        Get all routes, optionally filtered by user ID.

        Args:
            user_id: Optional user ID to filter routes by

        Returns:
            List of routes
        """
        pass

    @abstractmethod
    def update(self, route_id: UUID, route_data: Union[Route, dict]) -> Optional[Route]:
        """
        Update an existing route.

        Args:
            route_id: The ID of the route to update
            route_data: Updated route data, either as a Route object or dict

        Returns:
            The updated route if found, None otherwise
        """
        pass

    @abstractmethod
    def delete(self, route_id: UUID) -> bool:
        """
        Delete a route by its ID.

        Args:
            route_id: The ID of the route to delete

        Returns:
            True if deleted, False if not found
        """
        pass
