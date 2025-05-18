from abc import ABC, abstractmethod
from typing import BinaryIO


class StorageService(ABC):
    @abstractmethod
    def upload_file(self, file_data: BinaryIO, filename: str) -> str:
        """
        Upload a file to storage
        
        Args:
            file_data: The file data to upload
            filename: The name of the file
            
        Returns:
            The URL of the uploaded file
        """
        pass
    
    @abstractmethod
    def get_file_url(self, filename: str) -> str:
        """
        Get the URL for a file in storage
        
        Args:
            filename: The name of the file
            
        Returns:
            The URL of the file
        """
        pass
