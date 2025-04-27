import pytest
from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.application.queries.get_all_routes_query import GetAllRoutesQuery
from src.domain.entities.route import Route
from src.domain.entities.waypoint import Waypoint


class TestGetAllRoutesQuery:

    def setup_method(self):
        self.route_repository = MagicMock()
        self.query = GetAllRoutesQuery(route_repository=self.route_repository)

    def test_execute_returns_all_routes(self):
        # Arrange
        # Create mock routes to be returned by the repository
        user_ = uuid4()
        mock_routes = [
            Route(
                id=UUID('12345678-1234-5678-1234-567812345678'),
                name="Route 1",
                description="First test route",
                user_id=user_,
                waypoints=[]
            ),
            Route(
                id=UUID('87654321-4321-8765-4321-876543210987'),
                name="Route 2",
                description="Second test route",
                user_id=user_,
                waypoints=[
                    Waypoint(
                        id=UUID('12345678-1234-5678-1234-567812345679'),
                        latitude=40.7128,
                        longitude=-74.0060,
                        name="New York",
                        address="NY, USA",
                        order=0
                    )
                ]
            )
        ]

        # Set up the repository mock to return our routes
        self.route_repository.get_all.return_value = mock_routes

        # Act
        results = self.query.execute(user_id=user_)

        # Assert
        assert results is not None
        assert len(results) == 2
        assert results[0]["name"] == "Route 1"
        assert results[1]["name"] == "Route 2"
        assert len(results[1]["waypoints"]) == 1

        # Verify the repository was called with the correct filter
        self.route_repository.get_all.assert_called_once_with(filters={"user_id": user_})

    def test_execute_returns_empty_list_when_no_routes_found(self):
        # Arrange
        # Set up the repository mock to return an empty list
        self.route_repository.get_all.return_value = []

        # Act
        results = self.query.execute(user_id="user123")

        # Assert
        assert results == []

        # Verify the repository was called with the correct filter
        self.route_repository.get_all.assert_called_once_with(filters={"user_id": "user123"})
