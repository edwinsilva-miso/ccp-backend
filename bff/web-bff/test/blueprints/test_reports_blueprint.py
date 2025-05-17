import pytest
from unittest.mock import patch, MagicMock
import json
from flask import Flask
from src.blueprints.reports_blueprint import reports_blueprint


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(reports_blueprint)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


class TestReportsBlueprint:

    def test_get_report_by_user_id_unauthorized(self, client):
        # Test without authorization header
        response = client.get('/bff/v1/web/reports/user123')

        assert response.status_code == 401
        assert json.loads(response.data) == {'msg': 'Unauthorized'}

    @patch('src.blueprints.reports_blueprint.ReportsAdapter')
    def test_get_report_by_user_id_success(self, mock_adapter_class, client):
        # Arrange
        user_id = "user123"
        expected_response = {"reports": [{"id": "report1", "name": "Monthly Sales"}]}

        mock_adapter = MagicMock()
        mock_adapter_class.return_value = mock_adapter
        mock_adapter.get_report_by_user_id.return_value = (expected_response, 200)

        # Act
        response = client.get(
            f'/bff/v1/web/reports/{user_id}',
            headers={'Authorization': 'Bearer test_token'}
        )

        # Assert
        assert response.status_code == 200
        assert json.loads(response.data) == expected_response
        mock_adapter.get_report_by_user_id.assert_called_once_with('test_token', user_id)

    @patch('src.blueprints.reports_blueprint.ReportsAdapter')
    def test_get_report_by_user_id_not_found(self, mock_adapter_class, client):
        # Arrange
        user_id = "nonexistent"
        error_response = {"error": "User not found"}

        mock_adapter = MagicMock()
        mock_adapter_class.return_value = mock_adapter
        mock_adapter.get_report_by_user_id.return_value = (error_response, 404)

        # Act
        response = client.get(
            f'/bff/v1/web/reports/{user_id}',
            headers={'Authorization': 'Bearer test_token'}
        )

        # Assert
        assert response.status_code == 404
        assert json.loads(response.data) == error_response
        mock_adapter.get_report_by_user_id.assert_called_once_with('test_token', user_id)

    def test_generate_report_unauthorized(self, client):
        # Test without authorization header
        response = client.post(
            '/bff/v1/web/reports/generate',
            json={"userId": "user123", "type": "VENTAS_POR_MES"}
        )

        assert response.status_code == 401
        assert json.loads(response.data) == {'msg': 'Unauthorized'}

    @patch('src.blueprints.reports_blueprint.ReportsAdapter')
    def test_generate_report_success(self, mock_adapter_class, client):
        # Arrange
        report_data = {
            "userId": "user123",
            "type": "VENTAS_POR_MES",
            "filters": {"startDate": "2023-01-01", "endDate": "2023-01-31"}
        }
        expected_response = {
            "id": "report123",
            "userId": "user123",
            "name": "Sales Report",
            "date": "2023-02-01",
            "url": "https://storage.example.com/reports/report123.xlsx",
            "reportData": []
        }

        mock_adapter = MagicMock()
        mock_adapter_class.return_value = mock_adapter
        mock_adapter.generate_report.return_value = (expected_response, 200)

        # Act
        response = client.post(
            '/bff/v1/web/reports/generate',
            json=report_data,
            headers={'Authorization': 'Bearer test_token'}
        )

        # Assert
        assert response.status_code == 200
        assert json.loads(response.data) == expected_response
        mock_adapter.generate_report.assert_called_once_with('test_token', report_data)

    @patch('src.blueprints.reports_blueprint.ReportsAdapter')
    def test_generate_report_failure(self, mock_adapter_class, client):
        # Arrange
        report_data = {
            "userId": "user123",
            "type": "INVALID_TYPE",
            "filters": {}
        }
        error_response = {"error": "Invalid report type"}

        mock_adapter = MagicMock()
        mock_adapter_class.return_value = mock_adapter
        mock_adapter.generate_report.return_value = (error_response, 400)

        # Act
        response = client.post(
            '/bff/v1/web/reports/generate',
            json=report_data,
            headers={'Authorization': 'Bearer test_token'}
        )

        # Assert
        assert response.status_code == 400
        assert json.loads(response.data) == error_response
        mock_adapter.generate_report.assert_called_once_with('test_token', report_data)

    @patch('src.blueprints.reports_blueprint.ReportsAdapter')
    def test_token_with_bearer_prefix(self, mock_adapter_class, client):
        # Arrange
        user_id = "user123"
        expected_response = {"reports": [{"id": "report1"}]}

        mock_adapter = MagicMock()
        mock_adapter_class.return_value = mock_adapter
        mock_adapter.get_report_by_user_id.return_value = (expected_response, 200)

        # Act
        response = client.get(
            f'/bff/v1/web/reports/{user_id}',
            headers={'Authorization': 'Bearer test_token'}
        )

        # Assert
        assert response.status_code == 200
        mock_adapter.get_report_by_user_id.assert_called_once_with('test_token', user_id)

    @patch('src.blueprints.reports_blueprint.ReportsAdapter')
    def test_token_without_bearer_prefix(self, mock_adapter_class, client):
        # Arrange
        user_id = "user123"
        expected_response = {"reports": [{"id": "report1"}]}

        mock_adapter = MagicMock()
        mock_adapter_class.return_value = mock_adapter
        mock_adapter.get_report_by_user_id.return_value = (expected_response, 200)

        # Act
        response = client.get(
            f'/bff/v1/web/reports/{user_id}',
            headers={'Authorization': 'raw_token_without_bearer'}
        )

        # Assert
        assert response.status_code == 200
        mock_adapter.get_report_by_user_id.assert_called_once_with('raw_token_without_bearer', user_id)