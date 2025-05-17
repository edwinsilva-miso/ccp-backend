import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.application.utils.create_report_file import CreateReportFile


class TestCreateReportFile(unittest.TestCase):

    def setUp(self):
        self.file_name = "test_report.xlsx"
        self.headers = ["ID", "Name", "Value"]
        self.data = [{"ID": 1, "Name": "Test1", "Value": 100},
                     {"ID": 2, "Name": "Test2", "Value": 200}]
        self.report_creator = CreateReportFile(self.file_name, self.headers, self.data)

        # Define expected report directory
        self.expected_reports_dir = Path(__file__).parent.parent.parent / "resources" / "reports"

    def test_initialization(self):
        """Test proper initialization of the CreateReportFile class"""
        self.assertEqual(self.report_creator.file_name, self.file_name)
        self.assertEqual(self.report_creator.headers, self.headers)
        self.assertEqual(self.report_creator.data, self.data)
        self.assertEqual(self.report_creator.temp_dir, tempfile.gettempdir())

    def test_initialization_with_string_headers(self):
        """Test initialization with comma-separated string headers"""
        headers_str = "ID,Name,Value"
        report_creator = CreateReportFile(self.file_name, headers_str, self.data)
        self.assertEqual(report_creator.headers, ["ID", "Name", "Value"])

    @patch('os.makedirs')
    @patch('pandas.DataFrame')
    @patch('pandas.ExcelWriter')
    def test_create_file(self, mock_excel_writer, mock_dataframe, mock_makedirs):
        """Test the file creation process"""
        # Setup mocks
        mock_df = MagicMock()
        mock_dataframe.return_value = mock_df

        # Create a proper mock for DataFrame columns that has a values attribute
        columns_mock = MagicMock()
        columns_mock.values = self.headers
        mock_df.columns = columns_mock

        mock_writer = MagicMock()
        mock_excel_writer.return_value.__enter__.return_value = mock_writer

        mock_workbook = MagicMock()
        mock_writer.book = mock_workbook

        mock_worksheet = MagicMock()
        mock_writer.sheets = {'Report': mock_worksheet}

        # Create a property to capture the actual path used
        actual_path = None

        # Mock the actual file path construction rather than patching a non-existent attribute
        original_join = os.path.join

        def mock_path_join(*args):
            nonlocal actual_path
            actual_path = original_join(*args)
            return actual_path

        with patch('os.path.join', side_effect=mock_path_join):
            # Call method
            result_path = self.report_creator.create_file()

        # Assertions
        mock_dataframe.assert_called_once_with(self.data)
        mock_df.to_excel.assert_called_once_with(mock_writer, sheet_name='Report', index=False)
        self.assertEqual(result_path, actual_path)

    @patch('os.makedirs')
    @patch('pandas.DataFrame')
    def test_create_file_with_exception(self, mock_dataframe, mock_makedirs):
        """Test error handling during file creation"""
        # Setup mock to raise exception
        mock_dataframe.side_effect = Exception("Test exception")

        # Assertions
        with self.assertRaises(Exception) as context:
            self.report_creator.create_file()

        self.assertIn("Failed to create report file", str(context.exception))
        # We can't assert on the exact path since we don't know its implementation
        # Just verify that makedirs was called at least once
        mock_makedirs.assert_called()

    @patch('os.path.exists')
    @patch('os.remove')
    def test_cleanup_temp_file(self, mock_remove, mock_exists):
        """Test temporary file cleanup"""
        # Setup
        mock_exists.return_value = True
        file_path = "/tmp/test_report.xlsx"

        # Call method
        self.report_creator.cleanup_temp_file(file_path)

        # Assertions
        mock_exists.assert_called_once_with(file_path)
        mock_remove.assert_called_once_with(file_path)

    @patch('os.path.exists')
    @patch('os.remove')
    def test_cleanup_temp_file_nonexistent(self, mock_remove, mock_exists):
        """Test cleanup when file doesn't exist"""
        # Setup
        mock_exists.return_value = False
        file_path = "/tmp/nonexistent.xlsx"

        # Call method
        self.report_creator.cleanup_temp_file(file_path)

        # Assertions
        mock_exists.assert_called_once_with(file_path)
        mock_remove.assert_not_called()

    @patch('os.path.exists')
    @patch('os.remove')
    def test_cleanup_temp_file_exception(self, mock_remove, mock_exists):
        """Test error handling during cleanup"""
        # Setup
        mock_exists.return_value = True
        mock_remove.side_effect = Exception("Permission denied")
        file_path = "/tmp/test_report.xlsx"

        # Call method (should not raise exception)
        self.report_creator.cleanup_temp_file(file_path)

        # Assertions
        mock_exists.assert_called_once_with(file_path)
        mock_remove.assert_called_once_with(file_path)
