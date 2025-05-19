from typing import BinaryIO
from src.domain.ports.storage_service import StorageService
from src.domain.ports.storage_service import StorageService


class MockStorageService(StorageService):
    def __init__(self):
        self.uploaded_files = {}
    
    def upload_file(self, file_data, filename):
        self.uploaded_files[filename] = file_data.read()
        return f"gs://test-bucket/{filename}"
    
    def get_file_url(self, filename):
        return f"gs://test-bucket/{filename}"

class MockStorageService(StorageService):
    """
    A mock implementation of the StorageService for testing purposes.
    This avoids using GCS in tests.
    """
    
    def __init__(self, base_url="gs://mock-bucket"):
        """
        Initialize the mock storage service.
        
        Args:
            base_url: The base URL for mock storage
        """
        self.base_url = base_url
        self.uploaded_files = {}
        self.call_count = 0
    
    def upload_file(self, file_data: BinaryIO, filename: str) -> str:
        """
        Mock implementation that stores file data and returns a fake URL.
        
        Args:
            file_data: The file data to upload
            filename: The name of the file
            
        Returns:
            A fake URL for the uploaded file
        """
        self.call_count += 1
        
        # Read and store the file data if it's a file-like object
        if hasattr(file_data, 'read'):
            position = file_data.tell()
            content = file_data.read()
            file_data.seek(position)  # Reset position for further usage
            self.uploaded_files[filename] = content
        else:
            self.uploaded_files[filename] = file_data
        
        return self.get_file_url(filename)
    
    def get_file_url(self, filename: str) -> str:
        """
        Get a mock URL for a file.
        
        Args:
            filename: The name of the file
            
        Returns:
            A mock URL for the file
        """
        return f"{self.base_url}/{filename}"
