import unittest
from unittest.mock import MagicMock, patch

from src.application.get_reports_by_user import GetReportsByUser
from src.domain.entities.reports.order_reports_dto import OrderReportsDTO


class TestGetReportsByUser(unittest.TestCase):
    def setUp(self):
        # Create mock repository
        self.order_reports_repository = MagicMock()

        # Initialize the use case with mock repository
        self.get_reports_by_user = GetReportsByUser(self.order_reports_repository)

        # Sample test data
        self.user_id = "user123"
        self.sample_reports = [
            OrderReportsDTO(
                report_id="report1",
                user_id=self.user_id,
                report_name="report1.xlsx",
                report_date="2023-01-01T12:00:00Z",
                url="report1_url"
            ),
            OrderReportsDTO(
                report_id="report2",
                user_id=self.user_id,
                report_name="report2.xlsx",
                report_date="2023-01-02T14:30:00Z",
                url="report1_url"
            )
        ]

    def test_execute_returns_reports_from_repository(self):
        """Test that execute method returns reports from repository"""
        # Setup repository mock to return sample reports
        self.order_reports_repository.get_by_user_id.return_value = self.sample_reports

        # Call the method being tested
        result = self.get_reports_by_user.execute(self.user_id)

        # Verify repository was called with correct user_id
        self.order_reports_repository.get_by_user_id.assert_called_once_with(self.user_id)

        # Verify the result matches the expected reports
        self.assertEqual(result, self.sample_reports)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].report_id, "report1")
        self.assertEqual(result[1].report_id, "report2")

    def test_execute_with_empty_reports(self):
        """Test execute method when no reports are found"""
        # Setup repository mock to return empty list
        self.order_reports_repository.get_by_user_id.return_value = []

        # Call the method being tested
        result = self.get_reports_by_user.execute(self.user_id)

        # Verify repository was called with correct user_id
        self.order_reports_repository.get_by_user_id.assert_called_once_with(self.user_id)

        # Verify the result is an empty list
        self.assertEqual(result, [])
        self.assertEqual(len(result), 0)

    @patch('logging.Logger.debug')
    def test_logging_is_performed(self, mock_debug):
        """Test that logging is performed with the correct user ID"""
        # Setup repository mock
        self.order_reports_repository.get_by_user_id.return_value = self.sample_reports

        # Call the method being tested
        self.get_reports_by_user.execute(self.user_id)

        # Verify that logging was called with the correct message
        mock_debug.assert_called_once_with("Retrieving reports for user ID: %s", self.user_id)

    def test_execute_passes_repository_exceptions(self):
        """Test that exceptions from the repository are passed through"""
        # Setup repository mock to raise an exception
        self.order_reports_repository.get_by_user_id.side_effect = Exception("Database error")

        # Verify that the exception is passed through
        with self.assertRaises(Exception) as context:
            self.get_reports_by_user.execute(self.user_id)

        self.assertEqual(str(context.exception), "Database error")
        self.order_reports_repository.get_by_user_id.assert_called_once_with(self.user_id)


if __name__ == '__main__':
    unittest.main()
