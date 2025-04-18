import logging

from .errors.errors import InvalidFormatError, ProductAlreadyExistsError
from ..domain.entities.product_dto import ProductDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class CreateProduct:
    """
    Use case for creating a new product.
    """

    def __init__(self, repository):
        """
        Initializes the CreateProduct use case with a product repository.
        :param repository:
        """
        self.repository = repository

    def execute(self, product: ProductDTO) -> str:
        """
        Executes the creation of a product.
        :param product: The product to be created.
        :return: The created product.
        """
        logging.debug(f"Creating product {product.__str__()} ...")

        # Validate product information
        logging.debug("Validating product information...")

        # Check if price is a number and positive
        if not isinstance(product.price, (int, float)) or product.price <= 0:
            logging.error("Invalid price format. Price must be a positive number.")
            raise InvalidFormatError

        # Check if delivery time is a number and positive
        if not isinstance(product.delivery_time, int) or product.delivery_time <= 0:
            logging.error("Invalid delivery time format. Delivery time must be a positive number.")
            raise InvalidFormatError

        # Check if product already exists
        logging.debug("Checking if product already exists...")
        existing_product = self.repository.get_by_name(product.name)
        if existing_product:
            logging.error(f"Product {product.name} already exists.")
            raise ProductAlreadyExistsError

        logging.debug(f"Creating product {product.name}...")
        result = self.repository.add(product)

        logging.debug(f"Product {product.name} created successfully.")
        return result
