import logging

from .errors.errors import ProductNotExistsError
from ..domain.entities.product_dto import ProductDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class GetProductByManufacturer:
    """
    Use case for retrieving products by their manufacturer ID.
    """

    def __init__(self, repository):
        """
        Initializes the GetProductByManufacturer use case with a product repository.
        :param repository: An instance of ProductDTORepository.
        """
        self.repository = repository

    def execute(self, manufacturer_id: str) -> list[ProductDTO]:
        """
        Retrieves products by their manufacturer ID from the repository.
        :param manufacturer_id: The ID of the manufacturer whose products to retrieve.
        :return: A list of ProductDTO objects representing the products.
        """
        logging.debug(f"Retrieving products for manufacturer with ID {manufacturer_id}...")
        products = self.repository.get_by_manufacturer(manufacturer_id)
        if not products:
            logging.error(f"No products found for manufacturer with ID {manufacturer_id}.")
            raise ProductNotExistsError

        logging.debug(f"Products for manufacturer with ID {manufacturer_id} retrieved successfully.")
        return products
