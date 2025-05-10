import logging

from ..domain.entities.manufacturer_dto import ManufacturerDTO
from .errors.errors import ManufacturerNotExistsError

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class GetManufacturerByNit:
    """
    Use case for retrieving a manufacturer by its NIT.
    """

    def __init__(self, manufacturer_repository):
        """
        Initializes the GetManufacturerById use case with a manufacturer repository.
        :param manufacturer_repository: An instance of ManufacturerDTORepository.
        """
        self.manufacturer_repository = manufacturer_repository

    def execute(self, nit: str) -> ManufacturerDTO:
        """
        Retrieves a manufacturer by its NIT from the repository.
        :param nit: The NIT of the manufacturer to retrieve.
        :return: A ManufacturerDTO object representing the manufacturer.
        """
        logging.debug(f"Retrieving manufacturer with NIT {nit}...")
        manufacturer = self.manufacturer_repository.get_by_nit(nit)
        if not manufacturer:
            logging.error(f"Manufacturer with NIT {nit} not found.")
            raise ManufacturerNotExistsError

        logging.debug(f"Manufacturer with NIT {nit} retrieved successfully.")
        return manufacturer
