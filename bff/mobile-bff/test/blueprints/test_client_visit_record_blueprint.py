import unittest
from unittest.mock import patch, MagicMock
import json
from flask import Flask

from src.blueprints.client_visit_record_blueprint import client_visit_record_blueprint


class TestClientVisitRecordBlueprint(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(client_visit_record_blueprint)
        self.client = self.app.test_client()
        self.salesman_id = "123"
        self.record_id = "456"
        self.jwt_token = "test-jwt-token"
        self.headers = {'Authorization': f'Bearer {self.jwt_token}'}
        self.visit_data = {
            "clientId": "789",
            "visitDate": "2023-10-15",
            "notes": "Test visit"
        }

    @patch('src.adapters.client_visit_records_adapter.ClientVisitRecordsAdapter.get_client_visit_records')
    def test_get_client_visit_records_success(self, mock_get_records):
        # Setup mock
        mock_records = [
            {"id": "1", "salesmanId": self.salesman_id, "clientId": "789"},
            {"id": "2", "salesmanId": self.salesman_id, "clientId": "101"}
        ]
        mock_get_records.return_value = (mock_records, 200)

        # Make request
        response = self.client.get(
            f'/bff/v1/mobile/salesman/{self.salesman_id}/visits',
            headers=self.headers
        )

        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        mock_get_records.assert_called_once_with(self.jwt_token, self.salesman_id)

    def test_get_client_visit_records_unauthorized(self):
        # Test without auth header
        response = self.client.get(
            f'/bff/v1/mobile/salesman/{self.salesman_id}/visits'
        )

        # Assertions
        self.assertEqual(response.status_code, 401)

    @patch('src.adapters.client_visit_records_adapter.ClientVisitRecordsAdapter.get_client_visit_record')
    def test_get_client_visit_record_success(self, mock_get_record):
        # Setup mock
        mock_record = {
            "id": self.record_id,
            "salesmanId": self.salesman_id,
            "clientId": "789",
            "clientName": "Test Client",
            "store": "Test Store"
        }
        mock_get_record.return_value = (mock_record, 200)

        # Make request
        response = self.client.get(
            f'/bff/v1/mobile/salesman/{self.salesman_id}/visits/{self.record_id}',
            headers=self.headers
        )

        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["id"], self.record_id)
        self.assertEqual(data["clientName"], "Test Client")
        mock_get_record.assert_called_once_with(self.jwt_token, self.salesman_id, self.record_id)

    @patch('src.adapters.client_visit_records_adapter.ClientVisitRecordsAdapter.add_client_visit_record')
    def test_add_client_visit_record_success(self, mock_add_record):
        # Setup mock
        new_record = {
            "id": "new-id",
            "salesmanId": self.salesman_id,
            "clientId": "789",
            "visitDate": "2023-10-15",
            "notes": "Test visit"
        }
        mock_add_record.return_value = (new_record, 201)

        # Make request
        response = self.client.post(
            f'/bff/v1/mobile/salesman/{self.salesman_id}/visits',
            headers=self.headers,
            json=self.visit_data
        )

        # Assertions
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data["id"], "new-id")
        self.assertEqual(data["salesmanId"], self.salesman_id)
        mock_add_record.assert_called_once_with(self.jwt_token, self.salesman_id, self.visit_data)

    def test_add_client_visit_record_missing_fields(self):
        # Test with missing fields
        incomplete_data = {
            "clientId": "789",
            # Missing visitDate and notes
        }

        response = self.client.post(
            f'/bff/v1/mobile/salesman/{self.salesman_id}/visits',
            headers=self.headers,
            json=incomplete_data
        )

        # Assertions
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Faltan campos requeridos", data["msg"])


if __name__ == '__main__':
    unittest.main()