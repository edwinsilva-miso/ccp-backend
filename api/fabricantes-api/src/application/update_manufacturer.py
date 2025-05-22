import logging
import re

from .errors.errors import InvalidFormatError, ManufacturerNotExistsError
from .utils import constants
from ..domain.entities.manufacturer_dto import ManufacturerDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class UpdateManufacturer:
    """
    Use case for updating an existing manufacturer.
    """

    def __init__(self, manufacturer_repository):
        """
        Initializes the UpdateManufacturer use case with a manufacturer repository.
        :param manufacturer_repository: An instance of ManufacturerDTORepository.
        """
        self.manufacturer_repository = manufacturer_repository

    def execute(self, id: str, manufacturer: ManufacturerDTO) -> str:
        """
        Updates an existing manufacturer in the repository.
        :param id: The ID of the manufacturer to update.
        :param manufacturer: A ManufacturerDTO object representing the updated manufacturer data.
        :return: The ID of the updated manufacturer.
        """
        logging.debug(f"Updating manufacturer with ID {id}: {manufacturer.__str__()}")
        logging.debug("Validating manufacturer information...")
        email_pattern = constants.EMAIL_PATTERN
        if not re.match(email_pattern, manufacturer.email):
            logging.error("Invalid email format.")
            raise InvalidFormatError

        logging.debug(f"Checking if manufacturer with ID {id} exists...")
        existing_manufacturer = self.manufacturer_repository.get_by_id(id)
        if not existing_manufacturer:
            logging.error(f"manufacturer with ID {id} does not exist.")
            raise ManufacturerNotExistsError

        logging.debug(f"Updating manufacturer {id}...")
        manufacturer.id = id
        updated_manufacturer = self.manufacturer_repository.update(manufacturer)

        logging.debug(f"Manufacturer {id} updated successfully.")
        return updated_manufacturer
