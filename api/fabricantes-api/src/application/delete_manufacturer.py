import logging

from .errors.errors import ManufacturerNotExistsError

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

class DeleteManufacturer:
    """
    Use case for deleting a manufacturer by its ID.
    """

    def __init__(self, manufacturer_repository):
        """
        Initializes the DeleteManufacturer use case with a manufacturer repository.
        :param manufacturer_repository: An instance of ManufacturerRepository.
        """
        self.manufacturer_repository = manufacturer_repository

    def execute(self, id: str) -> None:
        """
        Deletes a manufacturer by its ID from the repository.
        :param id: The ID of the manufacturer to delete.
        """
        logging.debug(f"Deleting manufacturer with ID {id}...")

        # Check if the manufacturer exists before attempting to delete
        existing = self.manufacturer_repository.get_by_id(id)
        if not existing:
            logging.error(f"Manufacturer with ID {id} does not exist.")
            raise ManufacturerNotExistsError

        self.manufacturer_repository.delete(id)
        logging.debug(f"Manufacturer with ID {id} deleted successfully.")
