import logging
import os
from typing import BinaryIO
from google.cloud import storage
from src.domain.ports.storage_service import StorageService


class GCSStorageService(StorageService):
    def __init__(self):
        self.client = storage.Client()
        self.bucket_name = os.getenv("GCS_BUCKET_NAME", "").strip("'").strip('"')
        logging.debug(f"Using bucket name: '{self.bucket_name}'")
        self.bucket = self.client.bucket(self.bucket_name)

    def upload_file(self, file_data: BinaryIO, filename: str) -> str:
        """Upload a file to GCS bucket and return its URL"""
        try:
            logging.debug(f"Uploading {filename} to bucket {self.bucket_name}")

            # Reset file pointer to beginning
            if hasattr(file_data, 'seek'):
                file_data.seek(0)

            # Create a new blob and upload
            blob = self.bucket.blob(filename)
            blob.upload_from_file(file_data)
            logging.debug(f"Successfully uploaded {filename}")

            return self.get_file_url(filename)
        except Exception as e:
            logging.error(f"Upload error: {type(e).__name__}: {str(e)}")
            raise
    
    def get_file_url(self, filename: str) -> str:
        """Get the public URL for a file in GCS"""
        return f"gs://{self.bucket_name}/{filename}"
