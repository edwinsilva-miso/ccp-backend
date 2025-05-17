import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to sys.path to be able to import modules correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.adapters.reports_adapter import ReportsAdapter


class TestReportsAdapter(unittest.TestCase):

    def setUp(self):
        self.adapter = ReportsAdapter()
        self.test_jwt = "test_jwt_token"

    @patch('src.adapters.reports_adapter.requests.get')
    def test_get_report_by_user_id_success(self, mock_get):
        # Arrange
        user_id = "user123"
        expected_response = {"reports": [{"id": "report1", "name": "Monthly Sales"}]}

        mock_response = MagicMock()
        mock_response.json.return_value = expected_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Act
        result, status_code = self.adapter.get_report_by_user_id(self.test_jwt, user_id)

        # Assert
        mock_get.assert_called_once_with(
            f"http://localhost:5100/api/v1/reports/{user_id}",
            headers={'Authorization': f'Bearer {self.test_jwt}'}
        )
        self.assertEqual(result, expected_response)
        self.assertEqual(status_code, 200)

    @patch('src.adapters.reports_adapter.requests.post')
    def test_generate_report_basic_success(self, mock_post):
        # Arrange
        report_data = {
            "userId": "user123",
            "type": "VENTAS_POR_MES",
            "filters": {"startDate": "2023-01-01", "endDate": "2023-01-31"}
        }
        api_response = {
            "id": "report123",
            "userId": "user123",
            "name": "Sales Report",
            "date": "2023-02-01",
            "url": "https://storage.example.com/reports/report123.xlsx",
            "reportData": []
        }

        mock_response = MagicMock()
        mock_response.json.return_value = api_response
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Act
        result, status_code = self.adapter.generate_report(self.test_jwt, report_data)

        # Assert
        mock_post.assert_called_once_with(
            "http://localhost:5100/api/v1/reports/generate",
            headers={'Authorization': f'Bearer {self.test_jwt}'},
            json=report_data
        )
        self.assertEqual(status_code, 200)

    @patch('src.adapters.reports_adapter.requests.post')
    @patch('src.adapters.reports_adapter.ProductsAdapter')
    def test_generate_report_products_success(self, mock_products_adapter_class, mock_post):
        # Arrange
        report_data = {
            "userId": "user123",
            "type": "PRODUCTOS_MAS_VENDIDOS",
            "filters": {"startDate": "2023-01-01", "endDate": "2023-01-31"}
        }

        api_response = {
            "id": "report123",
            "userId": "user123",
            "name": "Product Sales Report",
            "date": "2023-02-01",
            "url": "https://storage.example.com/reports/report123.xlsx",
            "reportData": [
                {"productId": "prod1", "sales": 100},
                {"productId": "prod2", "sales": 75}
            ]
        }

        expected_decorated_response = {
            "id": "report123",
            "userId": "user123",
            "name": "Product Sales Report",
            "date": "2023-02-01",
            "url": "https://storage.example.com/reports/report123.xlsx",
            "reportData": [
                {"productId": "prod1", "sales": 100, "productName": "Product 1"},
                {"productId": "prod2", "sales": 75, "productName": "Product 2"}
            ]
        }

        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = api_response
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Mock products adapter
        mock_products_adapter = MagicMock()
        mock_products_adapter_class.return_value = mock_products_adapter
        mock_products_adapter.get_product_by_id.side_effect = [
            ({"id": "prod1", "name": "Product 1"}, 200),
            ({"id": "prod2", "name": "Product 2"}, 200)
        ]

        # Act
        result, status_code = self.adapter.generate_report(self.test_jwt, report_data)

        # Assert
        mock_post.assert_called_once_with(
            "http://localhost:5100/api/v1/reports/generate",
            headers={'Authorization': f'Bearer {self.test_jwt}'},
            json=report_data
        )
        self.assertEqual(mock_products_adapter.get_product_by_id.call_count, 2)
        mock_products_adapter.get_product_by_id.assert_any_call(self.test_jwt, "prod1")
        mock_products_adapter.get_product_by_id.assert_any_call(self.test_jwt, "prod2")
        self.assertEqual(result, expected_decorated_response)
        self.assertEqual(status_code, 200)

    @patch('src.adapters.reports_adapter.requests.post')
    def test_generate_report_failure(self, mock_post):
        # Arrange
        report_data = {
            "userId": "user123",
            "type": "INVALID_TYPE",
            "filters": {}
        }
        error_response = {"error": "Invalid report type"}

        mock_response = MagicMock()
        mock_response.json.return_value = error_response
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        # Act
        result, status_code = self.adapter.generate_report(self.test_jwt, report_data)

        # Assert
        mock_post.assert_called_once_with(
            "http://localhost:5100/api/v1/reports/generate",
            headers={'Authorization': f'Bearer {self.test_jwt}'},
            json=report_data
        )
        self.assertEqual(result, None)
        self.assertEqual(status_code, 400)

    @patch('src.adapters.reports_adapter.requests.get')
    def test_get_report_by_user_id_not_found(self, mock_get):
        # Arrange
        user_id = "nonexistent"
        error_response = {"error": "User not found"}

        mock_response = MagicMock()
        mock_response.json.return_value = error_response
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Act
        result, status_code = self.adapter.get_report_by_user_id(self.test_jwt, user_id)

        # Assert
        mock_get.assert_called_once_with(
            f"http://localhost:5100/api/v1/reports/{user_id}",
            headers={'Authorization': f'Bearer {self.test_jwt}'}
        )
        self.assertEqual(result, error_response)
        self.assertEqual(status_code, 404)