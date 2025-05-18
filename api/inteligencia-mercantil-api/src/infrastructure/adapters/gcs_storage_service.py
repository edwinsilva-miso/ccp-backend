import os
from typing import BinaryIO
from google.cloud import storage
from src.domain.ports.storage_service import StorageService


class GCSStorageService(StorageService):
    def __init__(self):
        self.client = storage.Client()
        self.bucket_name = os.getenv("GCS_BUCKET_NAME")
        self.bucket = self.client.bucket(self.bucket_name)

    def upload_file(self, file_data: BinaryIO, filename: str) -> str:
        """Upload a file to GCS bucket and return its URL"""
        blob = self.bucket.blob(filename)
        blob.upload_from_file(file_data)
        return self.get_file_url(filename)
    
    def get_file_url(self, filename: str) -> str:
        """Get the public URL for a file in GCS"""
        return f"gs://{self.bucket_name}/{filename}"
