import base64
import io
import logging
import pandas as pd
import re

from .errors.errors import InvalidFormatError
from .utils import constants
from ..domain.entities.manufacturer_dto import ManufacturerDTO

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class BulkCreateManufacturers:
    """
    Use case for creating multiple manufacturers from an Excel file.
    """

    def __init__(self, manufacturer_repository):
        """
        Initializes the BulkCreateManufacturers use case with a manufacturer repository.
        :param manufacturer_repository: An instance of ManufacturerDTORepository.
        """
        self.manufacturer_repository = manufacturer_repository

    def execute(self, excel_base64: str) -> dict:
        """
        Creates multiple manufacturers from an Excel file encoded in base64.

        :param excel_base64: Base64 encoded string of the Excel file.
        :return: Dictionary with results of the operation.
        """
        logging.debug("Starting bulk manufacturer creation process...")

        try:
            # Decode base64 string to bytes
            excel_data = base64.b64decode(excel_base64)

            # Read Excel file using pandas
            df = pd.read_excel(io.BytesIO(excel_data))

            # Initialize counters
            successful_count = 0
            failed_count = 0
            errors = []

            # Process each row in the Excel file
            for index, row in df.iterrows():
                try:

                    logging.debug("processing ." + str(index+1) + " row")

                    manufacturer = ManufacturerDTO(
                        id=None,
                        nit=str(row.get('NIT', '')),
                        name=str(row.get('NOMBRE', '')),
                        address=str(row.get('DIRECCION', '')),
                        phone=str(row.get('TELEFONO', '')),
                        email=str(row.get('CORREO', '')),
                        legal_representative=str(row.get('REPRESENTANTE LEGAL', '')),
                        country=str(row.get('PAIS', '')),
                        status=None,
                        created=None,
                        updated=None
                    )

                    # Validate manufacturer data
                    if self._validate_manufacturer(manufacturer):
                        # Check if manufacturer already exists
                        existing_manufacturer = self.manufacturer_repository.get_by_nit(manufacturer.nit)
                        if existing_manufacturer:
                            errors.append(f"Row {index+2}: Manufacturer with NIT {manufacturer.nit} already exists")
                            failed_count += 1
                            continue

                        # Check if manufacturer already exists by email
                        existing_email = self.manufacturer_repository.get_by_email(manufacturer.email)
                        if existing_email:
                            errors.append(f"Row {index+2}: Manufacturer with email {manufacturer.email} already exists")
                            failed_count += 1
                            continue

                        # Add manufacturer to repository
                        self.manufacturer_repository.add(manufacturer)
                        successful_count += 1
                    else:
                        errors.append(f"Row {index+2}: Invalid data format")
                        failed_count += 1

                except Exception as e:
                    errors.append(f"Row {index+2}: {str(e)}")
                    failed_count += 1
                    logging.error(f"Error processing row {index+2}: {str(e)}")

            logging.debug(f"Bulk creation completed. Successful: {successful_count}, Failed: {failed_count}")
            return {
                "successful_count": successful_count,
                "failed_count": failed_count,
                "errors": errors
            }

        except Exception as e:
            logging.error(f"Error processing Excel file: {str(e)}")
            raise e

    def _validate_manufacturer(self, manufacturer: ManufacturerDTO) -> bool:
        """
        Validates the manufacturer data.

        :param manufacturer: A ManufacturerDTO object to validate.
        :return: True if valid, False otherwise.
        """
        nit_pattern = constants.NIT_PATTERN
        email_pattern = constants.EMAIL_PATTERN
        logging.debug(f"Bulk creation completed. Successful: {manufacturer}")
        # Verify all required fields are present and not empty
        if not all([
            manufacturer.nit,
            manufacturer.name,
            manufacturer.address,
            manufacturer.phone,
            manufacturer.email,
            manufacturer.legal_representative,
            manufacturer.country
        ]):
            return False

        # Validate NIT and email formats
        if not re.match(nit_pattern, manufacturer.nit) or not re.match(email_pattern, manufacturer.email):
            return False

        return True