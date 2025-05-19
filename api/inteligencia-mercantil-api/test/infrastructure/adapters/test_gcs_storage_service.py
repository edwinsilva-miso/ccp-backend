import pytest
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO
import os

from src.infrastructure.adapters.gcs_storage_service import GCSStorageService


class TestGCSStorageService:
    @pytest.fixture
    def mock_storage_client(self):
        with patch('google.cloud.storage.Client') as mock_client:
            # Setup mock bucket and blob
            mock_bucket = MagicMock()
            mock_blob = MagicMock()
            
            # Configure client to return our mock bucket
            mock_client.return_value.bucket.return_value = mock_bucket
            
            # Configure bucket to return our mock blob
            mock_bucket.blob.return_value = mock_blob
            
            yield mock_client, mock_bucket, mock_blob
    
    @pytest.fixture
    def storage_service(self, mock_storage_client):
        # Set environment variable for the test
        os.environ["GCS_BUCKET_NAME"] = "test-bucket"
        
        # Create service with mocked client
        service = GCSStorageService()
        
        return service
    
    def test_init(self, mock_storage_client):
        """Test that the service initializes correctly"""
        # Arrange
        os.environ["GCS_BUCKET_NAME"] = "test-bucket"
        
        # Act
        service = GCSStorageService()
        
        # Assert
        mock_client, _, _ = mock_storage_client
        mock_client.assert_called_once()
        mock_client.return_value.bucket.assert_called_once_with("test-bucket")
        assert service.bucket_name == "test-bucket"
    
    def test_upload_file(self, storage_service, mock_storage_client):
        """Test that upload_file uploads a file and returns its URL"""
        # Arrange
        _, mock_bucket, mock_blob = mock_storage_client
        file_data = BytesIO(b"test content")
        filename = "test.mp4"
        
        # Act
        result = storage_service.upload_file(file_data, filename)
        
        # Assert
        mock_bucket.blob.assert_called_once_with(filename)
        mock_blob.upload_from_file.assert_called_once_with(file_data)
        assert result == f"gs://test-bucket/{filename}"
    
    def test_upload_file_error(self, storage_service, mock_storage_client):
        """Test that upload_file handles errors properly"""
        # Arrange
        _, mock_bucket, mock_blob = mock_storage_client
        mock_blob.upload_from_file.side_effect = Exception("Upload failed")
        file_data = BytesIO(b"test content")
        filename = "test.mp4"
        
        # Act/Assert
        with pytest.raises(Exception, match="Upload failed"):
            storage_service.upload_file(file_data, filename)
        
        mock_bucket.blob.assert_called_once_with(filename)
        mock_blob.upload_from_file.assert_called_once_with(file_data)
    
    def test_get_file_url(self, storage_service):
        """Test that get_file_url returns the correct URL"""
        # Arrange
        filename = "test.mp4"
        
        # Act
        result = storage_service.get_file_url(filename)
        
        # Assert
        assert result == f"gs://test-bucket/{filename}"
