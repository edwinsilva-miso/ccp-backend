import json
from unittest.mock import patch, Mock

import pytest
from src.application.errors.errors import ValidationApiError, ClientAlreadyAssociatedError
from src.domain.entities.client_salesman_dto import ClientSalesmanDTO
from src.interface.blueprints.client_salesman_blueprint import client_salesman_blueprint


@pytest.fixture
def app():
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(client_salesman_blueprint)

    # Configure app for testing
    app.config['TESTING'] = True

    # Mock container setup for token validation
    app.container = Mock()
    app.container.token_validator = Mock()

    return app


@pytest.fixture
def client(app):
    with app.test_client() as test_client:
        # Create application context for the test
        with app.app_context():
            yield test_client


class TestClientSalesmanBlueprint():
    def setup_method(self):
        self.test_salesman_id = "456"
        self.test_client_id = "789"
        self.client_salesman_id_1 = "123"
        self.client_salesman_id_2 = "456"
        self.valid_token = "valid_jwt_token"
        self.auth_header = {'Authorization': f'Bearer {self.valid_token}'}

        # Setup response DTO
        self.response_dto = ClientSalesmanDTO(
            id="new_id",
            salesman_id=self.test_salesman_id,
            client_id=self.test_client_id,
            client_name="Test Client",
            client_phone="123456789",
            client_email="test@example.com",
            address="Test Address",
            city="Test City",
            country="Test Country",
            store_name="Test Store"
        )

        # Sample client data
        self.sample_clients = [
            ClientSalesmanDTO(
                id=self.client_salesman_id_1,
                salesman_id=self.test_salesman_id,
                client_id="789",
                client_name="Test Client 1",
                client_phone="123456789",
                client_email="client1@example.com",
                address="Test Address 1",
                city="Test City 1",
                country="Test Country 1",
                store_name="Test Store 1"
            ),
            ClientSalesmanDTO(
                id=self.client_salesman_id_2,
                salesman_id=self.test_salesman_id,
                client_id="790",
                client_name="Test Client 2",
                client_phone="987654321",
                client_email="client2@example.com",
                address="Test Address 2",
                city="Test City 2",
                country="Test Country 2",
                store_name="Test Store 2"
            )
        ]

        # Sample request data for client association
        self.association_data = {
            "client": {
                "id": self.test_client_id,
                "name": "Test Client",
                "phone": "123456789",
                "email": "test@example.com"
            },
            "address": "Test Address",
            "city": "Test City",
            "country": "Test Country",
            "storeName": "Test Store"
        }

    @patch('src.interface.blueprints.client_salesman_blueprint.GetClientsBySalesman')
    @patch('src.interface.decorators.token_decorator.container')
    def test_get_clients_by_salesman(self, mock_container, mock_associate_client, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.test_salesman_id}
        mock_container.token_validator = mock_auth_service

        # Configure the use case mock
        mock_use_case = Mock()
        mock_use_case.execute.return_value = self.sample_clients
        mock_associate_client.return_value = mock_use_case

        # Make the request with a fake token
        response = client.get(
            f'/api/v1/salesman/{self.test_salesman_id}/clients',
            headers=self.auth_header
        )

        # Assertions
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]['id'] == self.client_salesman_id_1
        assert data[1]['id'] == self.client_salesman_id_2

        # Verify that the use case was called
        mock_use_case.execute.assert_called_once_with(self.test_salesman_id)

    @patch('src.interface.blueprints.client_salesman_blueprint.AssociateClient')
    @patch('src.interface.decorators.token_decorator.container')
    def test_associate_client_successfully(self, mock_container, mock_associate_client, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.test_salesman_id}
        mock_container.token_validator = mock_auth_service

        # Configure the use case mock
        mock_use_case = Mock()
        mock_use_case.execute.return_value = self.response_dto
        mock_associate_client.return_value = mock_use_case

        # Make the request with a fake token
        response = client.post(
            f'/api/v1/salesman/{self.test_salesman_id}/clients',
            json=self.association_data,
            headers=self.auth_header,
            content_type='application/json'
        )

        # Assertions
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['id'] == "new_id"
        assert data['salesmanId'] == self.test_salesman_id
        assert data['clientId'] == self.test_client_id

    @patch('src.interface.blueprints.client_salesman_blueprint.AssociateClient')
    @patch('src.interface.decorators.token_decorator.container')
    def test_associate_client_validation_error(self, mock_container, mock_associate_client, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.test_salesman_id}
        mock_container.token_validator = mock_auth_service

        # Configure the use case mock to raise ValidationApiError
        mock_use_case = Mock()
        mock_use_case.execute.side_effect = ValidationApiError
        mock_associate_client.return_value = mock_use_case

        # Make the request with a fake token
        response = client.post(
            f'/api/v1/salesman/{self.test_salesman_id}/clients',
            json=self.association_data,
            headers=self.auth_header,
            content_type='application/json'
        )

        # Assertions
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "msg" in data
        assert "Faltan campos requeridos." in data["msg"]

    @patch('src.interface.blueprints.client_salesman_blueprint.AssociateClient')
    @patch('src.interface.decorators.token_decorator.container')
    def test_associate_client_already_associated(self, mock_container, mock_associate_client, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.test_salesman_id}
        mock_container.token_validator = mock_auth_service

        # Configure the use case mock to raise ClientAlreadyAssociatedError
        mock_use_case = Mock()
        mock_use_case.execute.side_effect = ClientAlreadyAssociatedError
        mock_associate_client.return_value = mock_use_case

        # Make the request with a fake token
        response = client.post(
            f'/api/v1/salesman/{self.test_salesman_id}/clients',
            json=self.association_data,
            headers=self.auth_header,
            content_type='application/json'
        )

        # Assertions
        assert response.status_code == 412
        data = json.loads(response.data)
        assert "msg" in data
        assert "El cliente que intenta asociar ya existe. Por favor ingrese otro cliente." in data["msg"]

    @patch('src.interface.blueprints.client_salesman_blueprint.GetClientsBySalesman')
    @patch('src.interface.decorators.token_decorator.container')
    def test_get_clients_by_salesman_empty_list(self, mock_container, mock_get_clients, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.test_salesman_id}
        mock_container.token_validator = mock_auth_service

        # Configure the use case mock to return empty list
        mock_use_case = Mock()
        mock_use_case.execute.return_value = []
        mock_get_clients.return_value = mock_use_case

        # Make the request with a fake token
        response = client.get(
            f'/api/v1/salesman/{self.test_salesman_id}/clients',
            headers=self.auth_header
        )

        # Assertions
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0

    # AUTHENTICATION TESTS
    def test_missing_token(self, client):
        # Execute request without token
        response = client.get(f'/api/v1/salesman/{self.test_salesman_id}/clients')

        # Verify response
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data
        assert "Authorization header is missing" in data["error"]

    def test_invalid_token_format(self, client):
        # Execute request with invalid token format
        headers = {'Authorization': 'InvalidFormat token123'}
        response = client.get(f'/api/v1/salesman/{self.test_salesman_id}/clients', headers=headers)

        # Verify response
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data
        assert "Invalid authorization format" in data["error"]

    @patch('src.interface.decorators.token_decorator.container')
    def test_unauthorized_role(self, mock_container, client):
        # Mock token validation with unauthorized role
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "UNAUTHORIZED_ROLE", "user_id": "test-user"}
        mock_container.token_validator = mock_auth_service

        # Execute request
        response = client.get(f'/api/v1/salesman/{self.test_salesman_id}/clients', headers=self.auth_header)

        # Verify response
        assert response.status_code == 403
        data = json.loads(response.data)
        assert "error" in data
        assert "User does not have the required role" in data["error"]

    @patch('src.interface.decorators.token_decorator.container')
    def test_authentication_error(self, mock_container, client):
        # Mock token validation raising AuthenticationError
        from src.domain.exceptions.authentication_error import AuthenticationError

        mock_auth_service = Mock()
        mock_auth_service.validate_token.side_effect = AuthenticationError("Invalid or expired token")
        mock_container.token_validator = mock_auth_service

        # Execute request
        response = client.get(f'/api/v1/salesman/{self.test_salesman_id}/clients', headers=self.auth_header)

        # Verify response
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data
        assert "Invalid or expired token" in data["error"]

