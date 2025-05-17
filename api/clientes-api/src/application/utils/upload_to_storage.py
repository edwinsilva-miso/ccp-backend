import logging

from flask.cli import load_dotenv
from google.cloud import storage

from .create_report_file import CreateReportFile

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

load_dotenv()


class UploadToStorage:
    def __init__(self, storage_client=None):
        # Initialize storage client if not provided
        self.storage_client = storage_client or storage.Client()

    def upload(self, file_path, bucket_name, destination_blob_name) -> str:
        """
        Uploads a file to the specified bucket and returns the public URL.
        """
        try:
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(file_path)

            # construct the public URL directly
            public_url = f"https://storage.googleapis.com/{bucket_name}/{destination_blob_name}"

            logging.info(f"File {file_path} uploaded to {destination_blob_name}.")
            logging.info(f"Public URL: {public_url}")

            return public_url
        except Exception as e:
            logging.error(f"Error uploading file to GCS: {str(e)}")
            raise Exception(f"Failed to upload file to GCS: {str(e)}")

    def upload_report(self, file_name, headers, data, bucket_name="ccp-reports") -> str:
        """
        Creates an Excel report and uploads it to GCS bucket.

        Args:
            file_name: Name for the report file
            headers: Column headers for the report
            data: List of data records
            bucket_name: GCS bucket name (default: ccp_reports)

        Returns:
            Public URL of the uploaded file
        """
        try:
            # Create the report file
            report_creator = CreateReportFile(file_name, headers, data)
            file_path = report_creator.create_file()
            logging.info(f"Report file created at: {file_path}")

            # Upload to GCS
            public_url = self.upload(file_path, bucket_name, file_name)

            # Clean up the local file
            report_creator.cleanup_temp_file(file_path)

            return public_url
        except Exception as e:
            logging.error(f"Error in upload_report process: {str(e)}")
            raise Exception(f"Failed to create and upload report: {str(e)}")
