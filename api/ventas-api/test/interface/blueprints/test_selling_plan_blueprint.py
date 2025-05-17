import json
from unittest.mock import patch, Mock

import pytest
from src.application.errors.errors import ValidationApiError, ResourceNotFoundError
from src.domain.entities.selling_plan_dto import SellingPlanDTO
from src.interface.blueprints.selling_plan_blueprint import selling_plan_blueprint


@pytest.fixture
def app():
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(selling_plan_blueprint)

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


class TestSellingPlanBlueprint():
    def setup_method(self):
        self.test_user_id = "456"
        self.test_plan_id = "123"
        self.valid_token = "valid_jwt_token"
        self.auth_header = {'Authorization': f'Bearer {self.valid_token}'}

        # Setup response DTO
        self.response_dto = SellingPlanDTO(
            id="new_id",
            user_id=self.test_user_id,
            title="Test Plan",
            description="Test Description",
            target_amount=1000.0,
            target_date="2023-12-31",
            status="active"
        )

        # Sample selling plans
        self.sample_plans = [
            SellingPlanDTO(
                id="123",
                user_id=self.test_user_id,
                title="Test Plan 1",
                description="Test Description 1",
                target_amount=1000.0,
                target_date="2023-12-31",
                status="active"
            ),
            SellingPlanDTO(
                id="456",
                user_id=self.test_user_id,
                title="Test Plan 2",
                description="Test Description 2",
                target_amount=2000.0,
                target_date="2024-06-30",
                status="completed"
            )
        ]

        # Sample request data for plan creation
        self.plan_data = {
            "user_id": self.test_user_id,
            "title": "Test Plan",
            "description": "Test Description",
            "target_amount": 1000.0,
            "target_date": "2023-12-31",
            "status": "active"
        }

    # CREATE TESTS
    @patch('src.interface.blueprints.selling_plan_blueprint.CreateSellingPlan')
    @patch('src.interface.decorators.token_decorator.container')
    def test_create_selling_plan_successfully(self, mock_container, mock_create_selling_plan, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.test_user_id}
        mock_container.token_validator = mock_auth_service

        # Configure the use case mock
        mock_use_case = Mock()
        mock_use_case.execute.return_value = self.response_dto
        mock_create_selling_plan.return_value = mock_use_case

        # Make the request with a fake token
        response = client.post(
            '/api/v1/selling-plans',
            json=self.plan_data,
            headers=self.auth_header,
            content_type='application/json'
        )

        # Assertions
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['id'] == "new_id"
        assert data['user_id'] == self.test_user_id
        assert data['title'] == "Test Plan"

    @patch('src.interface.blueprints.selling_plan_blueprint.CreateSellingPlan')
    @patch('src.interface.decorators.token_decorator.container')
    def test_create_selling_plan_validation_error(self, mock_container, mock_create_selling_plan, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.test_user_id}
        mock_container.token_validator = mock_auth_service

        # Make the request with invalid data
        invalid_data = {"user_id": self.test_user_id}  # Missing required fields
        response = client.post(
            '/api/v1/selling-plans',
            json=invalid_data,
            headers=self.auth_header,
            content_type='application/json'
        )

        # Assertions
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "msg" in data
        assert "Faltan campos requeridos." in data["msg"]

    # UPDATE TESTS
    @patch('src.interface.blueprints.selling_plan_blueprint.UpdateSellingPlan')
    @patch('src.interface.decorators.token_decorator.container')
    def test_update_selling_plan_successfully(self, mock_container, mock_update_selling_plan, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.test_user_id}
        mock_container.token_validator = mock_auth_service

        # Configure the use case mock
        mock_use_case = Mock()
        mock_use_case.execute.return_value = self.response_dto
        mock_update_selling_plan.return_value = mock_use_case

        # Make the request with a fake token
        response = client.put(
            f'/api/v1/selling-plans/{self.test_plan_id}',
            json=self.plan_data,
            headers=self.auth_header,
            content_type='application/json'
        )

        # Assertions
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == "new_id"
        assert data['user_id'] == self.test_user_id
        assert data['title'] == "Test Plan"

    @patch('src.interface.blueprints.selling_plan_blueprint.UpdateSellingPlan')
    @patch('src.interface.decorators.token_decorator.container')
    def test_update_selling_plan_not_found(self, mock_container, mock_update_selling_plan, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.test_user_id}
        mock_container.token_validator = mock_auth_service

        # Configure the use case mock to raise ResourceNotFoundError
        mock_use_case = Mock()
        mock_use_case.execute.side_effect = ResourceNotFoundError
        mock_update_selling_plan.return_value = mock_use_case

        # Make the request with a fake token
        response = client.put(
            f'/api/v1/selling-plans/{self.test_plan_id}',
            json=self.plan_data,
            headers=self.auth_header,
            content_type='application/json'
        )

        # Assertions
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "msg" in data
        assert "El recurso solicitado no existe." in data["msg"]

    # GET BY ID TESTS
    @patch('src.interface.blueprints.selling_plan_blueprint.GetSellingPlanById')
    @patch('src.interface.decorators.token_decorator.container')
    def test_get_selling_plan_by_id_successfully(self, mock_container, mock_get_selling_plan, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.test_user_id}
        mock_container.token_validator = mock_auth_service

        # Configure the use case mock
        mock_use_case = Mock()
        mock_use_case.execute.return_value = self.sample_plans[0]
        mock_get_selling_plan.return_value = mock_use_case

        # Make the request with a fake token
        response = client.get(
            f'/api/v1/selling-plans/{self.test_plan_id}',
            headers=self.auth_header
        )

        # Assertions
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == "123"
        assert data['user_id'] == self.test_user_id
        assert data['title'] == "Test Plan 1"

    @patch('src.interface.blueprints.selling_plan_blueprint.GetSellingPlanById')
    @patch('src.interface.decorators.token_decorator.container')
    def test_get_selling_plan_by_id_not_found(self, mock_container, mock_get_selling_plan, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.test_user_id}
        mock_container.token_validator = mock_auth_service

        # Configure the use case mock to raise ResourceNotFoundError
        mock_use_case = Mock()
        mock_use_case.execute.side_effect = ResourceNotFoundError
        mock_get_selling_plan.return_value = mock_use_case

        # Make the request with a fake token
        response = client.get(
            f'/api/v1/selling-plans/{self.test_plan_id}',
            headers=self.auth_header
        )

        # Assertions
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "msg" in data
        assert "El recurso solicitado no existe." in data["msg"]

    # GET BY USER ID TESTS
    @patch('src.interface.blueprints.selling_plan_blueprint.GetSellingPlansByUserId')
    @patch('src.interface.decorators.token_decorator.container')
    def test_get_selling_plans_by_user_id_successfully(self, mock_container, mock_get_selling_plans, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.test_user_id}
        mock_container.token_validator = mock_auth_service

        # Configure the use case mock
        mock_use_case = Mock()
        mock_use_case.execute.return_value = self.sample_plans
        mock_get_selling_plans.return_value = mock_use_case

        # Make the request with a fake token
        response = client.get(
            f'/api/v1/selling-plans/user/{self.test_user_id}',
            headers=self.auth_header
        )

        # Assertions
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]['id'] == "123"
        assert data[1]['id'] == "456"

    @patch('src.interface.blueprints.selling_plan_blueprint.GetSellingPlansByUserId')
    @patch('src.interface.decorators.token_decorator.container')
    def test_get_selling_plans_by_user_id_empty_list(self, mock_container, mock_get_selling_plans, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.test_user_id}
        mock_container.token_validator = mock_auth_service

        # Configure the use case mock to return empty list
        mock_use_case = Mock()
        mock_use_case.execute.return_value = []
        mock_get_selling_plans.return_value = mock_use_case

        # Make the request with a fake token
        response = client.get(
            f'/api/v1/selling-plans/user/{self.test_user_id}',
            headers=self.auth_header
        )

        # Assertions
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0

    # DELETE TESTS
    @patch('src.interface.blueprints.selling_plan_blueprint.DeleteSellingPlan')
    @patch('src.interface.decorators.token_decorator.container')
    def test_delete_selling_plan_successfully(self, mock_container, mock_delete_selling_plan, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.test_user_id}
        mock_container.token_validator = mock_auth_service

        # Configure the use case mock
        mock_use_case = Mock()
        mock_use_case.execute.return_value = True
        mock_delete_selling_plan.return_value = mock_use_case

        # Make the request with a fake token
        response = client.delete(
            f'/api/v1/selling-plans/{self.test_plan_id}',
            headers=self.auth_header
        )

        # Assertions
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    @patch('src.interface.blueprints.selling_plan_blueprint.DeleteSellingPlan')
    @patch('src.interface.decorators.token_decorator.container')
    def test_delete_selling_plan_not_found(self, mock_container, mock_delete_selling_plan, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.test_user_id}
        mock_container.token_validator = mock_auth_service

        # Configure the use case mock to raise ResourceNotFoundError
        mock_use_case = Mock()
        mock_use_case.execute.side_effect = ResourceNotFoundError
        mock_delete_selling_plan.return_value = mock_use_case

        # Make the request with a fake token
        response = client.delete(
            f'/api/v1/selling-plans/{self.test_plan_id}',
            headers=self.auth_header
        )

        # Assertions
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "msg" in data
        assert "El recurso solicitado no existe." in data["msg"]

    # AUTHENTICATION TESTS
    def test_missing_token(self, client):
        # Execute request without token
        response = client.get(f'/api/v1/selling-plans/{self.test_plan_id}')

        # Verify response
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data
        assert "Authorization header is missing" in data["error"]

    def test_invalid_token_format(self, client):
        # Execute request with invalid token format
        headers = {'Authorization': 'InvalidFormat token123'}
        response = client.get(f'/api/v1/selling-plans/{self.test_plan_id}', headers=headers)

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
        response = client.get(f'/api/v1/selling-plans/{self.test_plan_id}', headers=self.auth_header)

        # Verify response
        assert response.status_code == 403
        data = json.loads(response.data)
        assert "error" in data
        assert "User does not have the required role" in data["error"]