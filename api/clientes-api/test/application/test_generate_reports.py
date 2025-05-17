import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
import uuid

from src.application.generate_reports import GenerateReports
from src.domain.entities.reports.order_reports_dto import OrderReportsDTO


class TestGenerateReports(unittest.TestCase):
    def setUp(self):
        # Create mock dependencies
        self.order_reports_repository = MagicMock()
        self.report_queries_adapter = MagicMock()

        # Initialize the use case with mock dependencies
        self.generate_reports = GenerateReports(
            self.order_reports_repository,
            self.report_queries_adapter
        )

        # Sample test data
        self.user_id = "user123"
        self.test_date = datetime.fromisoformat("2023-01-01T12:00:00")
        self.report_data = [{"month": "January", "sales": 1000}, {"month": "February", "sales": 1500}]
        self.report_headers = ["month", "sales"]

        # Mock return values for adapters
        self.report_queries_adapter.get_monthly_sales.return_value = {
            "headers": self.report_headers,
            "data": self.report_data
        }
        self.report_queries_adapter.get_monthly_product_sales.return_value = {
            "headers": ["product", "quantity"],
            "data": [{"product": "Product A", "quantity": 50}, {"product": "Product B", "quantity": 30}]
        }
        self.report_queries_adapter.get_monthly_sales_by_salesman.return_value = {
            "headers": ["salesman", "sales"],
            "data": [{"salesman": "John", "sales": 800}, {"salesman": "Jane", "sales": 1200}]
        }

        # Mock return value for repository
        sample_report = OrderReportsDTO(
            report_id="report-uuid",
            user_id=self.user_id,
            report_name="CCP_VENTAS_POR_MES_user123_20230101T120000.xlsx",
            report_date=self.test_date.isoformat(),
            url="https://storage.example.com/reports/report-uuid.xlsx"
        )
        self.order_reports_repository.add.return_value = sample_report

    @patch('uuid.uuid4')
    @patch('datetime.datetime')
    @patch('src.application.utils.upload_to_storage.UploadToStorage.upload_report')
    def test_execute_ventas_por_mes_report(self, mock_upload_report, mock_datetime, mock_uuid):
        """Test generating monthly sales report"""
        # Setup mocks
        mock_datetime.utcnow.return_value = self.test_date
        mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")

        # Mock the upload_report method directly
        mock_upload_report.return_value = "https://storage.example.com/reports/report-uuid.xlsx"

        # Test data
        request_data = {
            "userId": self.user_id,
            "type": "VENTAS_POR_MES",
            "filters": {
                "startDate": "2023-01-01",
                "endDate": "2023-01-31"
            }
        }

        # Execute the method
        result = self.generate_reports.execute(request_data)

        # Verify the report query adapter was called with correct params
        self.report_queries_adapter.get_monthly_sales.assert_called_once_with(
            start_date="2023-01-01",
            end_date="2023-01-31"
        )

        # Verify upload was called with correct params
        expected_report_name = f"CCP_VENTAS_POR_MES_{self.user_id}_{self.test_date.isoformat().translate(str.maketrans('', '', ':-'))}.xlsx"

        # Verify result contains expected fields
        self.assertEqual(result["userId"], self.user_id)
        self.assertEqual(result["name"], expected_report_name)
        self.assertEqual(result["reportData"], self.report_data)

    @patch('uuid.uuid4')
    @patch('datetime.datetime')
    @patch('src.application.utils.upload_to_storage.UploadToStorage.upload_report')
    def test_execute_productos_mas_vendidos_report(self, mock_upload_report, mock_datetime, mock_uuid):
        """Test generating top selling products report"""
        # Setup mocks
        mock_datetime.utcnow.return_value = self.test_date
        mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")

        # Mock the upload_report method directly
        mock_upload_report.return_value = "https://storage.example.com/reports/report-uuid.xlsx"

        # Mock product data - this should match what the adapter returns
        product_headers = ["product", "quantity"]
        product_data = [{"product": "Product A", "quantity": 50}, {"product": "Product B", "quantity": 30}]

        # Override repository return value for this specific test
        product_report = OrderReportsDTO(
            report_id="report-uuid",
            user_id=self.user_id,
            report_name=f"CCP_PRODUCTOS_MAS_VENDIDOS_{self.user_id}_20230101T120000.xlsx",
            report_date=self.test_date.isoformat(),
            url="https://storage.example.com/reports/report-uuid.xlsx"
        )
        self.order_reports_repository.add.return_value = product_report

        # Test data
        request_data = {
            "userId": self.user_id,
            "type": "PRODUCTOS_MAS_VENDIDOS",
            "filters": {
                "startDate": "2023-01-01",
                "endDate": "2023-01-31"
            }
        }

        # Execute the method
        result = self.generate_reports.execute(request_data)

        expected_report_name = f"CCP_PRODUCTOS_MAS_VENDIDOS_{self.user_id}_{self.test_date.isoformat().translate(str.maketrans('', '', ':-'))}.xlsx"
        # Verify result contains expected fields
        self.assertEqual(result["userId"], self.user_id)
        self.assertEqual(result["name"], expected_report_name)

    @patch('uuid.uuid4')
    @patch('datetime.datetime')
    @patch('src.application.utils.upload_to_storage.UploadToStorage.upload_report')
    def test_execute_ventas_por_vendedor_report(self, mock_upload_report, mock_datetime, mock_uuid):
        """Test generating sales by salesman report"""
        # Setup mocks
        mock_datetime.utcnow.return_value = self.test_date
        mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")

        # Mock the upload_report method directly
        mock_upload_report.return_value = "https://storage.example.com/reports/report-uuid.xlsx"

        # Mock salesman data - this should match what the adapter returns
        salesman_headers = ["salesman", "sales"]
        salesman_data = [{"salesman": "John", "sales": 800}, {"salesman": "Jane", "sales": 1200}]

        # Override repository return value for this specific test
        salesman_report = OrderReportsDTO(
            report_id="report-uuid",
            user_id=self.user_id,
            report_name=f"CCP_VENTAS_POR_VENDEDOR_{self.user_id}_20230101T120000.xlsx",
            report_date=self.test_date.isoformat(),
            url="https://storage.example.com/reports/report-uuid.xlsx"
        )
        self.order_reports_repository.add.return_value = salesman_report

        # Test data
        request_data = {
            "userId": self.user_id,
            "type": "VENTAS_POR_VENDEDOR",
            "filters": {
                "startDate": "2023-01-01",
                "endDate": "2023-01-31",
                "salesmanId": "salesman123"
            }
        }

        # Execute the method
        result = self.generate_reports.execute(request_data)

        # Verify upload was called with correct params
        expected_report_name = f"CCP_VENTAS_POR_VENDEDOR_{self.user_id}_{self.test_date.isoformat().translate(str.maketrans('', '', ':-'))}.xlsx"

        # Verify result contains expected fields
        self.assertEqual(result["userId"], self.user_id)
        self.assertEqual(result["name"], expected_report_name)

    @patch('uuid.uuid4')
    @patch('datetime.datetime')
    @patch('src.application.utils.upload_to_storage.UploadToStorage.upload_report')
    def test_execute_unknown_report_type(self, mock_upload_report, mock_datetime, mock_uuid):
        """Test handling unknown report type"""
        # Setup mocks
        mock_datetime.utcnow.return_value = self.test_date
        mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")

        # Mock the upload_report method directly
        mock_upload_report.return_value = "https://storage.example.com/reports/report-uuid.xlsx"

        # Test data with unknown report type
        request_data = {
            "userId": self.user_id,
            "type": "UNKNOWN_REPORT_TYPE",
            "filters": {
                "startDate": "2023-01-01",
                "endDate": "2023-01-31"
            }
        }

        # Execute the method
        result = self.generate_reports.execute(request_data)

        # Verify no report query methods were called
        self.report_queries_adapter.get_monthly_sales.assert_not_called()
        self.report_queries_adapter.get_monthly_product_sales.assert_not_called()
        self.report_queries_adapter.get_monthly_sales_by_salesman.assert_not_called()

        # Verify empty data was handled properly
        expected_report_name = f"CCP_UNKNOWN_REPORT_TYPE_{self.user_id}_{self.test_date.isoformat().translate(str.maketrans('', '', ':-'))}.xlsx"
        self.assertEqual(result["reportData"], [])

    @patch('logging.Logger.debug')
    @patch('uuid.uuid4')
    @patch('datetime.datetime')
    @patch('src.application.utils.upload_to_storage.UploadToStorage.upload_report')
    def test_execute_handles_upload_exception(self, mock_upload_report, mock_datetime, mock_uuid, mock_debug):
        """Test handling exceptions during file upload"""
        # Setup mocks
        mock_datetime.utcnow.return_value = self.test_date
        mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")

        # Configure upload to throw an exception
        mock_upload_report.side_effect = Exception("Failed to upload file")

        # Test data
        request_data = {
            "userId": self.user_id,
            "type": "VENTAS_POR_MES",
            "filters": {
                "startDate": "2023-01-01",
                "endDate": "2023-01-31"
            }
        }

        # Verify exception is propagated
        with self.assertRaises(Exception) as context:
            self.generate_reports.execute(request_data)

        self.assertTrue("Failed to upload file" in str(context.exception))

        # Verify repository was not called (since upload failed)
        self.order_reports_repository.add.assert_not_called()