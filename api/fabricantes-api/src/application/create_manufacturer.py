import logging
import re

from .errors.errors import InvalidFormatError, ManufacturerAlreadyExistsError
from .utils import constants
from ..domain.entities.manufacturer_dto import ManufacturerDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class CreateManufacturer:
    """
    Use case for creating a new manufacturer.
    """

    def __init__(self, manufacturer_repository):
        """
        Initializes the CreateManufacturer use case with a manufacturer repository.
        :param manufacturer_repository: An instance of ManufacturerDTORepository.
        """
        self.manufacturer_repository = manufacturer_repository

    def execute(self, manufacturer: ManufacturerDTO) -> str:
        """
        Creates a new manufacturer in the repository.
        :param manufacturer: A ManufacturerDTO object representing the manufacturer to create.
        :return: The ID of the created manufacturer.
        """
        logging.debug(f"Creating manufacturer: {manufacturer.__str__()}")

        logging.debug("Validating manufacturer information...")
        nit_pattern = constants.NIT_PATTERN
        email_pattern = constants.EMAIL_PATTERN

        if not re.match(nit_pattern, manufacturer.nit) or not re.match(email_pattern, manufacturer.email):
            logging.error("Invalid NIT or email format.")
            raise InvalidFormatError

        logging.debug(f"Checking if manufacturer {manufacturer.nit} already exists...")
        existing_manufacturer = self.manufacturer_repository.get_by_nit(manufacturer.nit)
        if existing_manufacturer:
            logging.error(f"manufacturer {manufacturer.nit} already exists.")
            raise ManufacturerAlreadyExistsError

        logging.debug(f"Creating manufacturer {manufacturer.nit}...")
        response = self.manufacturer_repository.add(manufacturer)

        logging.debug(f"Manufacturer {manufacturer.name} created successfully.")
        return response
