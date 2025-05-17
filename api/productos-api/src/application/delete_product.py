import logging

from .errors.errors import ProductNotExistsError

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class DeleteProduct:
    """
    Use case for deleting a product by its ID.
    """

    def __init__(self, repository):
        """
        Initializes the DeleteProduct use case with a product repository.
        :param repository: An instance of ProductDTORepository.
        """
        self.repository = repository

    def execute(self, product_id: str) -> None:
        """
        Deletes a product by its ID from the repository.
        :param product_id: The ID of the product to delete.
        :return: True if the product was deleted successfully, False otherwise.
        """
        logging.debug("Deleting product...")
        logging.debug("Checking if product exists...")
        existing = self.repository.get_by_id(product_id)
        if not existing:
            logging.error(f"Product with ID {product_id} not found.")
            raise ProductNotExistsError

        logging.debug(f"Deleting product with ID {product_id}...")
        self.repository.delete(product_id)

        logging.debug(f"Product with ID {product_id} deleted successfully.")
