import pytest
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4
from src.application.commands.update_route_command import UpdateRouteCommand
from src.domain.entities.route import Route
from src.domain.entities.waypoint import Waypoint
from src.domain.exceptions.domain_exceptions import RouteNotFoundError


class TestUpdateRouteCommand:

    def setup_method(self):
        self.route_repository = MagicMock()
        self.command = UpdateRouteCommand(route_repository=self.route_repository)
        self.route_service = self.command.route_service

    def test_execute_updates_route_successfully(self):
        # Arrange
        route_id = UUID('12345678-1234-5678-1234-567812345678')
        user_id = uuid4()

        route_data = {
            "name": "Updated Route Name",
            "description": "Updated route description",
            "user_id": user_id,
            "waypoints": [
                {
                    "latitude": 40.7128,
                    "longitude": -74.0060,
                    "name": "New York",
                    "address": "NY, USA"
                },
                {
                    "latitude": 34.0522,
                    "longitude": -118.2437,
                    "name": "Los Angeles",
                    "address": "CA, USA"
                }
            ]
        }

        # Create a mock updated route to be returned by the service
        mock_updated_route = Route(
            id=route_id,
            name="Updated Route Name",
            description="Updated route description",
            user_id=user_id,
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

        # Mock the route service's update_route method
        self.route_service.update_route = MagicMock(return_value=mock_updated_route)

        # Act
        result = self.command.execute(route_id, route_data)

        # Assert
        assert result is not None
        assert result["id"] == str(route_id)
        assert result["name"] == "Updated Route Name"
        assert result["description"] == "Updated route description"
        assert result["user_id"] == user_id
        assert len(result["waypoints"]) == 2
        assert result["waypoints"][0]["name"] == "New York"
        assert result["waypoints"][1]["name"] == "Los Angeles"

        # Verify that update_route was called with the correct arguments
        self.route_service.update_route.assert_called_once_with(
            route_id=route_id,
            updates=route_data
        )

    def test_execute_returns_none_when_route_not_found(self):
        # Arrange
        route_id = UUID('12345678-1234-5678-1234-567812345678')
        route_data = {
            "name": "Updated Route Name",
            "waypoints": []
        }

        # Mock the route service's update_route method to raise RouteNotFoundError
        self.route_service.update_route = MagicMock(side_effect=RouteNotFoundError("Route not found"))

        # Act
        result = self.command.execute(route_id, route_data)

        # Assert
        assert result is None

        # Verify that update_route was called with the correct arguments
        self.route_service.update_route.assert_called_once_with(
            route_id=route_id,
            updates=route_data
        )

    @patch('src.application.commands.update_route_command.validate_route_dto')
    def test_execute_with_invalid_data_raises_exception(self, mock_validate):
        # Arrange
        route_id = UUID('12345678-1234-5678-1234-567812345678')
        invalid_route_data = {
            "description": "Invalid route without name",
            "waypoints": []
        }

        # Mock validate_route_dto to raise a validation error
        mock_validate.side_effect = ValueError("Route validation failed: 'name' is required")

        # Act & Assert
        with pytest.raises(ValueError, match="Route validation failed: 'name' is required"):
            self.command.execute(route_id, invalid_route_data)

        # Verify validate_route_dto was called with the invalid data
        mock_validate.assert_called_once_with(invalid_route_data)

        # Verify update_route was not called
        assert not self.route_service.update_route.called

    def test_execute_with_partial_update(self):
        # Arrange
        route_id = UUID('12345678-1234-5678-1234-567812345678')
        user_ = uuid4()

        # Only updating name and description, not waypoints
        route_data = {
            "name": "Partially Updated Route",
            "description": "New description",
            "waypoints": []
        }

        # Create a mock updated route to be returned by the service
        mock_updated_route = Route(
            id=route_id,
            name="Partially Updated Route",
            description="New description",
            user_id=user_,
            waypoints=[]
        )

        # Mock the route service's update_route method
        self.route_service.update_route = MagicMock(return_value=mock_updated_route)

        # Act
        result = self.command.execute(route_id, route_data)

        # Assert
        assert result is not None
        assert result["id"] == str(route_id)
        assert result["name"] == "Partially Updated Route"
        assert result["description"] == "New description"
        assert len(result["waypoints"]) == 0

        # Verify that update_route was called with the correct arguments
        self.route_service.update_route.assert_called_once_with(
            route_id=route_id,
            updates=route_data
        )

    def test_execute_with_string_uuid(self):
        # Arrange
        route_id_str = "12345678-1234-5678-1234-567812345678"
        route_id = UUID(route_id_str)

        route_data = {
            "name": "New Route Name",
            "waypoints": []
        }

        # Create a mock updated route to be returned by the service
        mock_updated_route = Route(
            id=route_id,
            name="New Route Name",
            description=None,
            user_id=None,
            waypoints=[]
        )

        # Mock the route service's update_route method
        self.route_service.update_route = MagicMock(return_value=mock_updated_route)

        # Act
        result = self.command.execute(route_id, route_data)

        # Assert
        assert result is not None
        assert result["id"] == route_id_str
        assert result["name"] == "New Route Name"

        # Verify that update_route was called with the correct UUID object
        self.route_service.update_route.assert_called_once()
        call_args = self.route_service.update_route.call_args[1]
        assert call_args["route_id"] == route_id
