import pytest
from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.application.queries.get_route_query import GetRouteQuery
from src.domain.entities.route import Route
from src.domain.entities.waypoint import Waypoint


class TestGetRouteQuery:

    def setup_method(self):
        self.route_repository = MagicMock()
        self.query = GetRouteQuery(route_repository=self.route_repository)

    def test_execute_returns_route_when_exists(self):
        # Arrange
        route_id = UUID('12345678-1234-5678-1234-567812345678')
        user_ = uuid4()

        # Create a mock route to be returned by the repository
        mock_route = Route(
            id=route_id,
            name="Test Route",
            description="A test route",
            user_id=user_,
            waypoints=[
                Waypoint(
                    id=UUID('12345678-1234-5678-1234-567812345679'),
                    latitude=40.7128,
                    longitude=-74.0060,
                    name="New York",
                    address="NY, USA",
                    order=0
                ),
                Waypoint(
                    id=UUID('12345678-1234-5678-1234-567812345680'),
                    latitude=34.0522,
                    longitude=-118.2437,
                    name="Los Angeles",
                    address="CA, USA",
                    order=1
                )
            ]
        )

        # Set up the repository mock to return our route
        self.route_repository.get_by_id.return_value = mock_route

        # Act
        result = self.query.execute(route_id)

        # Assert
        assert result is not None
        assert result["id"] == str(route_id)
        assert result["name"] == "Test Route"
        assert result["description"] == "A test route"
        assert len(result["waypoints"]) == 2

        # Verify the repository was called with the correct ID
        self.route_repository.get_by_id.assert_called_once_with(route_id)

    def test_execute_returns_none_when_route_not_found(self):
        # Arrange
        route_id = UUID('12345678-1234-5678-1234-567812345678')

        # Set up the repository mock to return None (route not found)
        self.route_repository.get_by_id.return_value = None

        # Act
        result = self.query.execute(route_id)

        # Assert
        assert result is None

        # Verify the repository was called with the correct ID
        self.route_repository.get_by_id.assert_called_once_with(route_id)

    def test_execute_with_invalid_id_format_raises_exception(self):
        # Arrange
        invalid_id = "not-a-uuid"

        # Act & Assert
        with pytest.raises(ValueError):
            self.query.execute(invalid_id)
