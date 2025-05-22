import unittest
from unittest.mock import patch, MagicMock
import json

from src.adapters.client_visit_records_adapter import ClientVisitRecordsAdapter


class TestClientVisitRecordsAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = ClientVisitRecordsAdapter()
        self.jwt = "test-jwt-token"
        self.salesman_id = "123"
        self.record_id = "456"
        self.visit_data = {
            "clientId": "789",
            "visitDate": "2023-10-15",
            "notes": "Test visit"
        }

    @patch('requests.get')
    @patch('src.adapters.client_visit_records_adapter.ClientVisitRecordsAdapter._decorate_response')
    def test_get_client_visit_records_success(self, mock_decorate, mock_get):
        # Setup mock responses
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": "1", "salesmanId": self.salesman_id, "clientId": "789"},
            {"id": "2", "salesmanId": self.salesman_id, "clientId": "101"}
        ]
        mock_get.return_value = mock_response

        # Setup decorator mock to return same data
        mock_decorate.side_effect = lambda jwt, record: record

        # Call the method
        result, status_code = self.adapter.get_client_visit_records(self.jwt, self.salesman_id)

        # Assertions
        mock_get.assert_called_once_with(
            f"http://localhost:5106/api/v1/sales/api/v1/salesman/{self.salesman_id}/visits",
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(len(result), 2)
        self.assertEqual(mock_decorate.call_count, 2)

    @patch('requests.get')
    def test_get_client_visit_records_error(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "Not found"}
        mock_get.return_value = mock_response

        # Call the method
        result, status_code = self.adapter.get_client_visit_records(self.jwt, self.salesman_id)

        # Assertions
        self.assertEqual(status_code, 404)
        self.assertEqual(result, {"error": "Not found"})

    @patch('requests.get')
    @patch('src.adapters.client_visit_records_adapter.ClientVisitRecordsAdapter._decorate_response')
    def test_get_client_visit_record_success(self, mock_decorate, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": self.record_id, "salesmanId": self.salesman_id, "clientId": "789"}
        mock_get.return_value = mock_response

        # Setup decorator mock
        mock_decorate.return_value = {
            "id": self.record_id,
            "salesmanId": self.salesman_id,
            "clientId": "789",
            "clientName": "Test Client",
            "store": "Test Store"
        }

        # Call the method
        result, status_code = self.adapter.get_client_visit_record(self.jwt, self.salesman_id, self.record_id)

        # Assertions
        mock_get.assert_called_once_with(
            f"http://localhost:5106/api/v1/sales/api/v1/salesman/{self.salesman_id}/visits/{self.record_id}",
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(result["id"], self.record_id)
        self.assertEqual(result["clientName"], "Test Client")
        self.assertEqual(result["store"], "Test Store")

    @patch('requests.post')
    def test_add_client_visit_record(self, mock_post):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "new-id",
            "salesmanId": self.salesman_id,
            "clientId": self.visit_data["clientId"],
            "visitDate": self.visit_data["visitDate"],
            "notes": self.visit_data["notes"]
        }
        mock_post.return_value = mock_response

        # Call the method
        result, status_code = self.adapter.add_client_visit_record(self.jwt, self.salesman_id, self.visit_data)

        # Assertions
        mock_post.assert_called_once_with(
            f"http://localhost:5106/api/v1/sales/api/v1/salesman/{self.salesman_id}/visits",
            json=self.visit_data,
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        self.assertEqual(status_code, 201)
        self.assertEqual(result["salesmanId"], self.salesman_id)
        self.assertEqual(result["clientId"], self.visit_data["clientId"])

    @patch('src.adapters.salesman_adapter.SalesmanAdapter.get_clients_by_salesman')
    def test_decorate_response_with_client_data(self, mock_get_clients):
        # Setup test data
        record = {
            "id": "123",
            "salesmanId": self.salesman_id,
            "clientId": "789",
            "visitDate": "2023-10-15"
        }

        # Mock the clients response
        mock_get_clients.return_value = (
            [
                {
                    "clientId": "789",
                    "clientName": "Test Client",
                    "storeName": "Test Store"
                }
            ],
            200
        )

        # Call the method
        result = self.adapter._decorate_response(self.jwt, record)

        # Assertions
        mock_get_clients.assert_called_once_with(self.jwt, self.salesman_id)
        self.assertEqual(result["clientName"], "Test Client")
        self.assertEqual(result["store"], "Test Store")

    @patch('src.adapters.salesman_adapter.SalesmanAdapter.get_clients_by_salesman')
    def test_decorate_response_client_not_found(self, mock_get_clients):
        # Setup test data
        record = {
            "id": "123",
            "salesmanId": self.salesman_id,
            "clientId": "999",  # Different from available client
            "visitDate": "2023-10-15"
        }

        # Mock the clients response
        mock_get_clients.return_value = (
            [
                {
                    "clientId": "789",
                    "clientName": "Test Client",
                    "storeName": "Test Store"
                }
            ],
            200
        )

        # Call the method
        result = self.adapter._decorate_response(self.jwt, record)

        # Assertions
        self.assertNotIn("clientName", result)
        self.assertNotIn("store", result)


if __name__ == '__main__':
    unittest.main()