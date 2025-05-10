import logging

from ..domain.entities.manufacturer_dto import ManufacturerDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class GetAllManufacturers:
    """
    Use case for retrieving all manufacturers.
    """

    def __init__(self, manufacturer_repository):
        """
        Initializes the GetAllManufacturers use case with a manufacturer repository.
        :param manufacturer_repository: An instance of ManufacturerDTORepository.
        """
        self.manufacturer_repository = manufacturer_repository

    def execute(self) -> list[ManufacturerDTO]:
        """
        Retrieves all manufacturers from the repository.
        :return: A list of ManufacturerDTO objects.
        """
        logging.debug("Retrieving all manufacturers...")
        return self.manufacturer_repository.get_all()
