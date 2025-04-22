import logging

from .errors.errors import ProductNotExistsError
from ..domain.entities.product_dto import ProductDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class GetProductById:
    """
    Use case for retrieving a product by its ID.
    """

    def __init__(self, repository):
        """
        Initializes the GetProductById use case with a product repository.
        :param repository: An instance of ProductDTORepository.
        """
        self.repository = repository

    def execute(self, product_id: str) -> ProductDTO:
        """
        Retrieves a product by its ID from the repository.
        :param product_id: The ID of the product to retrieve.
        :return: A ProductDTO object representing the product.
        """
        logging.debug(f"Retrieving product with ID {product_id}...")
        product = self.repository.get_by_id(product_id)
        if not product:
            logging.error(f"Product with ID {product_id} not found.")
            raise ProductNotExistsError

        logging.debug(f"Product with ID {product_id} retrieved successfully.")
        return product
