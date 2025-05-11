import json
import uuid
from datetime import datetime
from unittest.mock import patch, Mock

import pytest
from src.application.errors.errors import ValidationApiError, RecordNotExistsError
from src.domain.entities.client_visit_record_dto import ClientVisitRecordDTO
from src.interface.blueprints.client_visit_record_blueprint import client_visit_record_blueprint


@pytest.fixture
def app():
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(client_visit_record_blueprint)

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


class TestClientVisitRecordBlueprint():
    def setup_method(self):
        # Sample data for testing
        self.salesman_id = str(uuid.uuid4())
        self.record_id = str(uuid.uuid4())
        self.client_id = str(uuid.uuid4())
        self.visit_date = datetime.now().isoformat()
        self.notes = "Test visit notes"
        self.valid_token = "valid_jwt_token"
        self.auth_header = {'Authorization': f'Bearer {self.valid_token}'}

        # Mock client visit record
        self.sample_visit_record = ClientVisitRecordDTO(
            record_id=self.record_id,
            salesman_id=self.salesman_id,
            client_id=self.client_id,
            visit_date=self.visit_date,
            notes=self.notes
        )

    @patch('src.interface.blueprints.client_visit_record_blueprint.GetVisitsBySalesman')
    @patch('src.interface.decorators.token_decorator.container')
    def test_get_visits_by_salesman(self, mock_container, mock_get_visits_by_salesman, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.salesman_id}
        mock_container.token_validator = mock_auth_service

        # Setup mock
        mock_use_case = Mock()
        mock_get_visits_by_salesman.return_value = mock_use_case
        mock_use_case.execute.return_value = [self.sample_visit_record, self.sample_visit_record]

        # Make request
        response = client.get(f'/api/v1/salesman/{self.salesman_id}/visits', headers=self.auth_header)

        # Assertions
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data) == 2
        mock_use_case.execute.assert_called_once_with(self.salesman_id)

    @patch('src.interface.blueprints.client_visit_record_blueprint.GetVisitsBySalesman')
    @patch('src.interface.decorators.token_decorator.container')
    def test_get_visits_by_salesman_empty_id(self, mock_container, mock_get_visits_by_salesman, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.salesman_id}
        mock_container.token_validator = mock_auth_service

        # Setup mock
        mock_use_case = Mock()
        mock_get_visits_by_salesman.return_value = mock_use_case
        mock_use_case.execute.return_value = []

        # Make request
        response = client.get(f'/api/v1/salesman/{self.salesman_id}/visits', headers=self.auth_header)

        # Assertions
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data) == 0
        mock_use_case.execute.assert_called_once_with(self.salesman_id)

    @patch('src.interface.blueprints.client_visit_record_blueprint.AddClientVisit')
    @patch('src.interface.decorators.token_decorator.container')
    def test_add_client_visit(self, mock_container, mock_add_client_visit, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.salesman_id}
        mock_container.token_validator = mock_auth_service

        # Setup mock
        mock_use_case = Mock()
        mock_add_client_visit.return_value = mock_use_case
        mock_use_case.execute.return_value = self.record_id

        # Request data
        request_data = {
            'clientId': self.client_id,
            'visitDate': self.visit_date,
            'notes': self.notes
        }

        # Make request
        response = client.post(
            f'/api/v1/salesman/{self.salesman_id}/visits',
            data=json.dumps(request_data),
            headers=self.auth_header,
            content_type='application/json'
        )

        # Assertions
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert response_data['id'] == self.record_id
        mock_use_case.execute.assert_called_once()

    @patch('src.interface.blueprints.client_visit_record_blueprint.AddClientVisit')
    @patch('src.interface.decorators.token_decorator.container')
    def test_add_client_visit_missing_fields(self, mock_container, mock_add_client_visit, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.salesman_id}
        mock_container.token_validator = mock_auth_service

        # Configure the use case mock to raise ValidationApiError
        mock_use_case = Mock()
        mock_use_case.execute.side_effect = ValidationApiError
        mock_add_client_visit.return_value = mock_use_case

        # Request data with missing fields
        request_data = {
            'clientId': self.client_id,
            # Missing visitDate and notes
        }

        # Make request
        response = client.post(
            f'/api/v1/salesman/{self.salesman_id}/visits',
            data=json.dumps(request_data),
            headers=self.auth_header,
            content_type='application/json'
        )

        # Assertions
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "msg" in data
        assert "Faltan campos requeridos." in data["msg"]

    @patch('src.interface.blueprints.client_visit_record_blueprint.GetClientVisitRecord')
    @patch('src.interface.decorators.token_decorator.container')
    def test_get_client_visit_record(self, mock_container, mock_get_client_visit_record, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.salesman_id}
        mock_container.token_validator = mock_auth_service

        # Setup mock
        mock_use_case = Mock()
        mock_get_client_visit_record.return_value = mock_use_case
        mock_use_case.execute.return_value = self.sample_visit_record

        # Make request
        response = client.get(f'/api/v1/salesman/{self.salesman_id}/visits/{self.record_id}', headers=self.auth_header)

        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['recordId'] == self.record_id
        mock_use_case.execute.assert_called_once_with(self.record_id)

    @patch('src.interface.blueprints.client_visit_record_blueprint.GetClientVisitRecord')
    @patch('src.interface.decorators.token_decorator.container')
    def test_get_client_visit_record_not_found(self, mock_container, mock_use_case_class, client):
        # Mock token validator
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "VENDEDOR", "user_id": self.salesman_id}
        mock_container.token_validator = mock_auth_service

        # Configure the use case mock to raise ValidationApiError
        # Setup mock to raise RecordNotExistsError
        mock_use_case = Mock()
        mock_use_case.execute.side_effect = RecordNotExistsError()
        mock_use_case_class.return_value = mock_use_case

        # Make request with error handling
        response = client.get(f'/api/v1/salesman/{self.salesman_id}/visits/{self.record_id}', headers=self.auth_header)

        assert response.status_code == 404
        data = json.loads(response.data)
        assert "msg" in data
        assert "El registro de visita de cliente no existe en el sistema." in data["msg"]
