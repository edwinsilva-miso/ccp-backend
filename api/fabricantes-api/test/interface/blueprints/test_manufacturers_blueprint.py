import json
from unittest.mock import patch, ANY

import pytest
from flask import Flask
from src.application.errors.errors import (
    ManufacturerNotExistsError,
    ManufacturerAlreadyExistsError,
    InvalidFormatError
)
from src.domain.entities.manufacturer_dto import ManufacturerDTO
from src.infrastructure.config.container import DependencyContainer
from src.interface.blueprints.manufacturers_blueprint import manufacturers_blueprint, token_required


class TestManufacturersBlueprint:
    @pytest.fixture
    def app(self):
        """Create and configure a Flask app for testing."""
        app = Flask(__name__)
        app.register_blueprint(manufacturers_blueprint)
        app.config['TESTING'] = True

        @app.errorhandler(ManufacturerNotExistsError)
        def handle_not_exists_error(error):
            return {"msg": "El fabricante no existe."}, 404

        @app.errorhandler(ManufacturerAlreadyExistsError)
        def handle_already_exists_error(error):
            return {"msg": "Manufacturer already exists"}, 409

        @app.errorhandler(InvalidFormatError)
        def handle_invalid_format_error(error):
            return {"msg": "Invalid format"}, 400

        return app

    @pytest.fixture
    def client(self, app):
        """A test client for the app."""
        return app.test_client()

    @pytest.fixture
    def auth_headers(self):
        """Mock authorization headers for token_required decorator."""
        return {
            'Authorization': 'Bearer test-token'
        }

    @pytest.fixture
    def sample_manufacturer(self):
        return ManufacturerDTO(
            id="test-id-123",
            name="Test Manufacturer",
            nit="1234567890",
            address="123 Test St.",
            phone="123-456-7890",
            email="test@example.com",
            legal_representative="Test Rep",
            country="Test Country",
            status="ACTIVO",
            created="2023-01-01T00:00:00",
            updated="2023-01-01T00:00:00"
        )

    @pytest.fixture
    def sample_manufacturers(self):
        return [
            ManufacturerDTO(
                id="test-id-1",
                name="Manufacturer 1",
                nit="1111111111",
                address="123 First St.",
                phone="111-111-1111",
                email="first@example.com",
                legal_representative="Rep One",
                country="Country One",
                status="ACTIVO",
                created="2023-01-01T00:00:00",
                updated="2023-01-01T00:00:00"
            ),
            ManufacturerDTO(
                id="test-id-2",
                name="Manufacturer 2",
                nit="2222222222",
                address="456 Second St.",
                phone="222-222-2222",
                email="second@example.com",
                legal_representative="Rep Two",
                country="Country Two",
                status="ACTIVO",
                created="2023-01-01T00:00:00",
                updated="2023-01-01T00:00:00"
            )
        ]

    @pytest.fixture(autouse=True)
    def mock_token_validator(self):
        """Mock the token validator to prevent API calls."""
        with patch('src.infrastructure.config.container.DependencyContainer.token_validator') as mock:
            mock.validate_token.return_value = {
                "email": "mail@example.com",
                "role": "DIRECTIVO"  # Only DIRECTIVO role is allowed
            }
            yield mock

    @pytest.fixture(autouse=True)
    def mock_token_required(self):
        """Mock the token_required decorator."""
        with patch('src.interface.decorators.token_decorator.token_required', lambda f: f):
            yield

    @patch('src.interface.blueprints.manufacturers_blueprint.GetAllManufacturers')
    def test_get_all_manufacturers(self, mock_get_all, client, sample_manufacturers, auth_headers):
        # Arrange
        mock_get_all.return_value.execute.return_value = sample_manufacturers

        # Act
        response = client.get('/api/v1/manufacturers/', headers=auth_headers)

        # Assert
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]['id'] == 'test-id-1'
        assert data[1]['id'] == 'test-id-2'
        assert data[0]['name'] == 'Manufacturer 1'
        assert data[1]['name'] == 'Manufacturer 2'

        # Verify use case was called
        mock_get_all.return_value.execute.assert_called_once()

    @patch('src.interface.blueprints.manufacturers_blueprint.GetManufacturerById')
    def test_get_manufacturer_by_id_success(self, mock_get_by_id, client, sample_manufacturer, auth_headers):
        # Arrange
        mock_get_by_id.return_value.execute.return_value = sample_manufacturer

        # Act
        response = client.get('/api/v1/manufacturers/test-id-123', headers=auth_headers)

        # Assert
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['id'] == 'test-id-123'
        assert data['name'] == 'Test Manufacturer'
        assert data['nit'] == '1234567890'

        # Verify use case was called with correct ID
        mock_get_by_id.return_value.execute.assert_called_once_with('test-id-123')

    @patch('src.interface.blueprints.manufacturers_blueprint.GetManufacturerById')
    def test_get_manufacturer_by_id_not_found(self, mock_get_by_id, client, auth_headers):
        # Arrange
        mock_get_by_id.return_value.execute.side_effect = ManufacturerNotExistsError

        # Act
        response = client.get('/api/v1/manufacturers/nonexistent-id', headers=auth_headers)

        # Assert
        assert response.status_code == 404

        data = json.loads(response.data)
        assert data['msg'] == 'El fabricante no existe.'

        # Verify use case was called with correct ID
        mock_get_by_id.return_value.execute.assert_called_once_with('nonexistent-id')

    @patch('src.interface.blueprints.manufacturers_blueprint.GetManufacturerByNit')
    def test_get_manufacturer_by_nit_success(self, mock_get_by_nit, client, sample_manufacturer, auth_headers):
        # Arrange
        mock_get_by_nit.return_value.execute.return_value = sample_manufacturer
        query_params = {'nit': '1234567890'}

        # Act
        response = client.get('/api/v1/manufacturers/search', query_string={'nit': '1234567890'}, headers=auth_headers)

        # Assert
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['id'] == 'test-id-123'
        assert data['name'] == 'Test Manufacturer'
        assert data['nit'] == '1234567890'

        # Verify use case was called with correct NIT
        mock_get_by_nit.return_value.execute.assert_called_once_with('1234567890')

    def test_get_manufacturer_by_nit_missing_param(self, client, auth_headers):
        # Arrange
        query_params = {'nit': None}

        # Act
        response = client.get('/api/v1/manufacturers/search', query_string=query_params, headers=auth_headers)

        # Assert
        assert response.status_code == 400

        data = json.loads(response.data)
        assert data['msg'] == 'Faltan campos requeridos.'

    @patch('src.interface.blueprints.manufacturers_blueprint.CreateManufacturer')
    def test_create_manufacturer_success(self, mock_create, client, sample_manufacturer, auth_headers):
        # Arrange
        mock_create.return_value.execute.return_value = sample_manufacturer.id

        manufacturer_data = {
            "name": "Test Manufacturer",
            "nit": "1234567890",
            "address": "123 Test St.",
            "phone": "123-456-7890",
            "email": "test@example.com",
            "legal_representative": "Test Rep",
            "country": "Test Country"
        }

        # Act
        response = client.post(
            '/api/v1/manufacturers/',
            data=json.dumps(manufacturer_data),
            content_type='application/json',
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 201

        data = json.loads(response.data)
        assert data['id'] == sample_manufacturer.id

        # Verify use case was called with manufacturer data
        mock_create.return_value.execute.assert_called_once()

    def test_create_manufacturer_missing_fields(self, client, auth_headers):
        # Arrange
        manufacturer_data = {
            "name": "Test Manufacturer"
        }

        # Act
        response = client.post(
            '/api/v1/manufacturers/',
            data=json.dumps(manufacturer_data),
            content_type='application/json',
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 400

        data = json.loads(response.data)
        assert data['msg'] == 'Faltan campos requeridos.'

    @patch('src.interface.blueprints.manufacturers_blueprint.UpdateManufacturer')
    def test_update_manufacturer_success(self, mock_update, client, sample_manufacturer, auth_headers):
        # Arrange
        mock_update.return_value.execute.return_value = sample_manufacturer

        update_data = {
            "name": "Updated Manufacturer",
            "address": "456 Updated St.",
            "phone": "987-654-3210",
            "email": "updated@example.com",
            "legal_representative": "Updated Rep",
            "country": "Updated Country",
            "status": "INACTIVO"
        }

        # Act
        response = client.put(
            '/api/v1/manufacturers/test-id-123',
            data=json.dumps(update_data),
            content_type='application/json',
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200

        # Verify use case was called with manufacturer data
        mock_update.return_value.execute.assert_called_once_with('test-id-123', ANY)

    def test_update_manufacturer_missing_fields(self, client, auth_headers):
        # Arrange
        update_data = {
            "name": "Updated Manufacturer"
        }

        # Act
        response = client.put(
            '/api/v1/manufacturers/test-id-123',
            data=json.dumps(update_data),
            content_type='application/json',
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['msg'] == 'Faltan campos requeridos.'

    @patch('src.interface.blueprints.manufacturers_blueprint.DeleteManufacturer')
    def test_delete_manufacturer_success(self, mock_delete, client, auth_headers):
        # Arrange
        mock_delete.return_value.execute.return_value = None

        # Act
        response = client.delete('/api/v1/manufacturers/test-id-123', headers=auth_headers)

        # Assert
        assert response.status_code == 204

        # Verify use case was called with correct ID
        mock_delete.return_value.execute.assert_called_once_with('test-id-123')
