import io
import logging
import os
import tempfile
from pathlib import Path

import pandas as pd

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class CreateReportFile:
    """
    Class to create a report file.
    """

    def __init__(self, file_name: str, headers: str, data: list):
        self.file_name = file_name
        self.headers = headers.split(',') if isinstance(headers, str) else headers
        self.data = data
        # Use tempdir for temporary storage
        self.temp_dir = tempfile.gettempdir()

    def create_file(self) -> str:
        """
        Create an Excel report file in a structured reports directory.
        :return: Path to the created file
        """
        logging.debug(f"Creating report file: {self.file_name}")

        try:
            # Create a structured path for reports
            self.reports_dir = Path(__file__).parent.parent.parent / "resources" / "reports"
            os.makedirs(self.reports_dir, exist_ok=True)

            # Create full file path in reports directory
            file_path = os.path.join(self.reports_dir, self.file_name)

            # Convert list of dictionaries to DataFrame
            df = pd.DataFrame(self.data)

            # If headers were provided, rename the columns
            if len(self.headers) == len(df.columns):
                df.columns = self.headers

            # Write DataFrame to Excel with formatting
            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Report', index=False)

                # Get the xlsxwriter objects
                workbook = writer.book
                worksheet = writer.sheets['Report']

                # Add header formatting
                header_format = workbook.add_format({
                    'bold': True,
                    'text_wrap': True,
                    'valign': 'top',
                    'bg_color': '#D7E4BC',
                    'border': 1
                })

                # Apply header format
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)

                # Auto-adjust columns' width
                for i, col in enumerate(df.columns):
                    column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
                    worksheet.set_column(i, i, column_width)

            logging.debug(f"Excel report successfully created at: {file_path}")
            return file_path

        except Exception as e:
            logging.error(f"Error creating Excel report: {str(e)}")
            raise Exception(f"Failed to create report file: {str(e)}")

    def cleanup_temp_file(self, file_path: str) -> None:
        """
        Remove temporary file after upload to GCS.
        :param file_path: Path to the temporary file to be removed
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.debug(f"Temporary file removed: {file_path}")
        except Exception as e:
            logging.warning(f"Failed to remove temporary file {file_path}: {str(e)}")
