import pytest
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4
from src.application.commands.create_route_command import CreateRouteCommand
from src.domain.entities.route import Route
from src.domain.entities.waypoint import Waypoint
from src.domain.services.route_service import RouteService


class TestCreateRouteCommand:

    def setup_method(self):
        self.route_repository = MagicMock()
        self.command = CreateRouteCommand(route_repository=self.route_repository)
        self.route_service = self.command.route_service

    def test_execute_creates_route_successfully(self):
        # Arrange
        user_id = uuid4()
        route_data = {
            "name": "Test Route",
            "description": "A test route description",
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

        # Create a mock route to be returned by the service
        mock_route = Route(
            id=UUID('12345678-1234-5678-1234-567812345678'),
            name="Test Route",
            description="A test route description",
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

        # Mock the route service's create_route method
        self.route_service.create_route = MagicMock(return_value=mock_route)

        # Act
        result = self.command.execute(route_data)

        # Assert
        assert result is not None
        assert result["id"] == str(mock_route.id)
        assert result["name"] == "Test Route"
        assert result["description"] == "A test route description"
        assert result["user_id"] == user_id
        assert len(result["waypoints"]) == 2
        assert result["waypoints"][0]["name"] == "New York"
        assert result["waypoints"][1]["name"] == "Los Angeles"

        # Verify that create_route was called with the correct arguments
        self.route_service.create_route.assert_called_once()
        call_args = self.route_service.create_route.call_args[1]
        assert call_args["name"] == "Test Route"
        assert call_args["description"] == "A test route description"
        assert call_args["user_id"] == user_id
        assert len(call_args["waypoints"]) == 2
        assert call_args["waypoints"][0].latitude == 40.7128
        assert call_args["waypoints"][0].longitude == -74.0060
        assert call_args["waypoints"][0].order == 0
        assert call_args["waypoints"][1].latitude == 34.0522
        assert call_args["waypoints"][1].longitude == -118.2437
        assert call_args["waypoints"][1].order == 1

    def test_execute_with_minimal_valid_data(self):
        # Arrange
        route_data = {
            "name": "Minimal Route",
            "waypoints": [
                {
                    "latitude": 40.7128,
                    "longitude": -74.0060
                }
            ]
        }

        # Create a mock route to be returned by the service
        mock_route = Route(
            id=UUID('12345678-1234-5678-1234-567812345678'),
            name="Minimal Route",
            description=None,
            user_id=None,
            waypoints=[
                Waypoint(
                    id=UUID('12345678-1234-5678-1234-567812345679'),
                    latitude=40.7128,
                    longitude=-74.0060,
                    name=None,
                    address=None,
                    order=0
                )
            ]
        )

        # Mock the route service's create_route method
        self.route_service.create_route = MagicMock(return_value=mock_route)

        # Act
        result = self.command.execute(route_data)

        # Assert
        assert result is not None
        assert result["name"] == "Minimal Route"
        assert result["description"] is None
        assert len(result["waypoints"]) == 1
        assert result["waypoints"][0]["latitude"] == 40.7128
        assert result["waypoints"][0]["longitude"] == -74.0060
        assert result["waypoints"][0]["name"] is None
        assert result["waypoints"][0]["address"] is None

        # Verify that create_route was called with the correct arguments
        self.route_service.create_route.assert_called_once()
        call_args = self.route_service.create_route.call_args[1]
        assert call_args["name"] == "Minimal Route"
        assert call_args["description"] is None
        assert call_args["user_id"] is None
        assert len(call_args["waypoints"]) == 1

    @patch('src.application.commands.create_route_command.validate_route_dto')
    def test_execute_with_invalid_data_raises_exception(self, mock_validate):
        # Arrange
        invalid_route_data = {
            "description": "Invalid route without name",
            "waypoints": []
        }

        # Mock validate_route_dto to raise a validation error
        mock_validate.side_effect = ValueError("Route validation failed: 'name' is required")

        # Act & Assert
        with pytest.raises(ValueError, match="Route validation failed: 'name' is required"):
            self.command.execute(invalid_route_data)

        # Verify validate_route_dto was called with the invalid data
        mock_validate.assert_called_once_with(invalid_route_data)

        # Verify create_route was not called
        assert not self.route_service.create_route.called

    def test_execute_preserves_waypoint_order(self):
        # Arrange
        route_data = {
            "name": "Ordered Route",
            "waypoints": [
                {
                    "latitude": 40.7128,
                    "longitude": -74.0060,
                    "name": "First Stop"
                },
                {
                    "latitude": 38.9072,
                    "longitude": -77.0369,
                    "name": "Second Stop"
                },
                {
                    "latitude": 34.0522,
                    "longitude": -118.2437,
                    "name": "Third Stop"
                }
            ]
        }

        # Create a mock route to be returned by the service
        mock_route = Route(
            id=UUID('12345678-1234-5678-1234-567812345678'),
            name="Ordered Route",
            description=None,
            user_id=None,
            waypoints=[
                Waypoint(
                    id=UUID('12345678-1234-5678-1234-567812345679'),
                    latitude=40.7128,
                    longitude=-74.0060,
                    name="First Stop",
                    address=None,
                    order=0
                ),
                Waypoint(
                    id=UUID('12345678-1234-5678-1234-567812345680'),
                    latitude=38.9072,
                    longitude=-77.0369,
                    name="Second Stop",
                    address=None,
                    order=1
                ),
                Waypoint(
                    id=UUID('12345678-1234-5678-1234-567812345681'),
                    latitude=34.0522,
                    longitude=-118.2437,
                    name="Third Stop",
                    address=None,
                    order=2
                )
            ]
        )

        # Mock the route service's create_route method
        self.route_service.create_route = MagicMock(return_value=mock_route)

        # Act
        result = self.command.execute(route_data)

        # Assert
        assert result is not None
        assert len(result["waypoints"]) == 3
        assert result["waypoints"][0]["name"] == "First Stop"
        assert result["waypoints"][1]["name"] == "Second Stop"
        assert result["waypoints"][2]["name"] == "Third Stop"

        # Verify the order of waypoints passed to the service
        self.route_service.create_route.assert_called_once()
        call_args = self.route_service.create_route.call_args[1]
        waypoints = call_args["waypoints"]
        assert len(waypoints) == 3
        assert waypoints[0].name == "First Stop"
        assert waypoints[0].order == 0
        assert waypoints[1].name == "Second Stop"
        assert waypoints[1].order == 1
        assert waypoints[2].name == "Third Stop"
        assert waypoints[2].order == 2
