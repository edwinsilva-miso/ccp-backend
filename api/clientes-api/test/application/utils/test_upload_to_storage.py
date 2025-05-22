import unittest
from unittest.mock import MagicMock, patch

from src.application.utils.upload_to_storage import UploadToStorage


class TestUploadToStorage(unittest.TestCase):

    def setUp(self):
        # Create mock storage client and related objects
        self.mock_storage_client = MagicMock()
        self.mock_bucket = MagicMock()
        self.mock_blob = MagicMock()

        # Configure mocks
        self.mock_storage_client.bucket.return_value = self.mock_bucket
        self.mock_bucket.blob.return_value = self.mock_blob

        # Initialize with mock storage client
        self.uploader = UploadToStorage(storage_client=self.mock_storage_client)

    def test_upload_success(self):
        # Test data
        file_path = "/path/to/test_file.xlsx"
        bucket_name = "test-bucket"
        destination_blob_name = "reports/test_file.xlsx"

        # Call method
        result = self.uploader.upload(file_path, bucket_name, destination_blob_name)

        # Assertions
        self.mock_storage_client.bucket.assert_called_once_with(bucket_name)
        self.mock_bucket.blob.assert_called_once_with(destination_blob_name)
        self.mock_blob.upload_from_filename.assert_called_once_with(file_path)

        expected_url = f"https://storage.googleapis.com/{bucket_name}/{destination_blob_name}"
        self.assertEqual(result, expected_url)

    def test_upload_error(self):
        # Test data
        file_path = "/path/to/test_file.xlsx"
        bucket_name = "test-bucket"
        destination_blob_name = "reports/test_file.xlsx"

        # Configure mock to raise exception
        self.mock_blob.upload_from_filename.side_effect = Exception("Upload failed")

        # Assertions
        with self.assertRaises(Exception) as context:
            self.uploader.upload(file_path, bucket_name, destination_blob_name)

        self.assertIn("Failed to upload file to GCS", str(context.exception))

    @patch('src.application.utils.upload_to_storage.CreateReportFile')
    def test_upload_report_success(self, mock_create_report):
        # Test data
        file_name = "test_report.xlsx"
        headers = ["ID", "Name", "Value"]
        data = [{"ID": 1, "Name": "Test", "Value": 100}]
        bucket_name = "test-bucket"

        # Configure mock CreateReportFile
        mock_report_instance = MagicMock()
        mock_create_report.return_value = mock_report_instance
        mock_report_instance.create_file.return_value = "/tmp/test_report.xlsx"

        # Mock upload method
        self.uploader.upload = MagicMock(return_value="https://storage.googleapis.com/test-bucket/test_report.xlsx")

        # Call method
        result = self.uploader.upload_report(file_name, headers, data, bucket_name)

        # Assertions
        mock_create_report.assert_called_once_with(file_name, headers, data)
        mock_report_instance.create_file.assert_called_once()
        self.uploader.upload.assert_called_once_with("/tmp/test_report.xlsx", bucket_name, file_name)
        mock_report_instance.cleanup_temp_file.assert_called_once_with("/tmp/test_report.xlsx")

        expected_url = "https://storage.googleapis.com/test-bucket/test_report.xlsx"
        self.assertEqual(result, expected_url)

    @patch('src.application.utils.upload_to_storage.CreateReportFile')
    def test_upload_report_create_file_error(self, mock_create_report):
        # Test data
        file_name = "test_report.xlsx"
        headers = ["ID", "Name", "Value"]
        data = [{"ID": 1, "Name": "Test", "Value": 100}]

        # Configure mock to raise exception during file creation
        mock_report_instance = MagicMock()
        mock_create_report.return_value = mock_report_instance
        mock_report_instance.create_file.side_effect = Exception("File creation failed")

        # Assertions
        with self.assertRaises(Exception) as context:
            self.uploader.upload_report(file_name, headers, data)

        self.assertIn("Failed to create and upload report", str(context.exception))

    def test_upload_report_default_bucket(self):
        # Test data
        file_name = "test_report.xlsx"
        headers = ["ID", "Name", "Value"]
        data = [{"ID": 1, "Name": "Test", "Value": 100}]

        # Mock the necessary methods to avoid actual execution
        with patch.object(self.uploader, 'upload',
                          return_value="https://storage.googleapis.com/ccp-reports/test_report.xlsx") as mock_upload:
            with patch('src.application.utils.upload_to_storage.CreateReportFile') as mock_create_report:
                # Configure CreateReportFile mock
                mock_report_instance = MagicMock()
                mock_create_report.return_value = mock_report_instance
                mock_report_instance.create_file.return_value = "/tmp/test_report.xlsx"

                # Call method without specifying bucket_name
                result = self.uploader.upload_report(file_name, headers, data)

                # Verify default bucket was used
                mock_upload.assert_called_once_with("/tmp/test_report.xlsx", "ccp-reports", file_name)
                self.assertEqual(result, "https://storage.googleapis.com/ccp-reports/test_report.xlsx")


if __name__ == '__main__':
    unittest.main()
