from unittest.mock import MagicMock, patch
from uuid import UUID
from uuid import uuid4

import pytest

from src.application.commands.create_route_command import CreateRouteCommand
from src.domain.entities.route import Route
from src.domain.entities.waypoint import Waypoint


class TestCreateRouteCommand:

    def setup_method(self):
        self.route_repository = MagicMock()
        self.command = CreateRouteCommand(route_repository=self.route_repository)
        self.route_service = self.command.route_service

    def test_execute_creates_route_successfully(self, db_session, sample_route_data):
        # Arrange
        from datetime import datetime
        from unittest.mock import Mock
        from src.infrastructure.repositories.sqlalchemy_route_repository import Route, Waypoint  # adjust based on your imports

        # Create mock waypoints
        mock_waypoints = [
            Waypoint(
                latitude=10.0,
                longitude=20.0,
                name="Waypoint 1",
                address="Address 1",
                order=0,
                id=UUID("c31c553c-5447-493e-abd1-aafe3ba6e1b1"),
                created_at=datetime.now(),
            ),
            Waypoint(
                latitude=30.0,
                longitude=40.0,
                name="Waypoint 2",
                address="Address 2",
                order=1,
                id=UUID("13188ba2-a839-4426-8d4b-14eb04f4e482"),
                created_at=datetime.now(),
            ),
        ]

        # Create mock Route object
        expected_route = Route(
            name="Sample Route",
            waypoints=mock_waypoints,
            user_id=UUID("201832fe-28c9-41f2-80e5-5482776d7c80"),
            id=UUID("ca77e138-b632-41ca-8a03-88fd1c4ab6ae"),
            description="some description",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        # Mock the repository create method to return the Route object
        repository_mock = Mock()
        repository_mock.create.return_value = expected_route
        command = CreateRouteCommand(route_repository=repository_mock)

        # Act
        result = command.execute(sample_route_data)

        # Assert
        assert result is not None
        assert result["name"] == sample_route_data["name"]
        assert "waypoints" in result
        assert len(result["waypoints"]) == len(sample_route_data["waypoints"])

        # Verify the repository was called with the correct Route object
        repository_mock.create.assert_called_once()
        created_route = repository_mock.create.call_args[0][0]  # Extract the Route object passed
        assert isinstance(created_route, Route)
        assert created_route.name == expected_route.name
        assert created_route.description == expected_route.description
        assert created_route.user_id == expected_route.user_id
        assert len(created_route.waypoints) == len(expected_route.waypoints)

    def test_execute_with_minimal_valid_data(self):
        # Arrange
        route_data = {
            "id": uuid4(),
            "name": "Minimal Route",
            "waypoints": [
                {
                    "id": uuid4(),
                    "latitude": 40.7128,
                    "longitude": -74.0060
                }
            ]
        }

        # Create a mock route to be returned by the service
        mock_route = Route(
            id=uuid4(),
            name="Minimal Route",
            description=None,
            user_id=None,
            waypoints=[
                Waypoint(
                    id=uuid4(),
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
