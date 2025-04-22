import logging

from .errors.errors import InvalidFormatError, ProductNotExistsError
from ..domain.entities.product_dto import ProductDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class UpdateProduct:
    """
    Use case for updating a product in the repository.
    """

    def __init__(self, repository):
        self.repository = repository

    def execute(self, product_id: str, product: ProductDTO) -> ProductDTO:
        """
        Executes the update of a product.
        :param product_id: The ID of the product to be updated.
        :param product: The product data to be updated.
        :return: The updated product.
        """
        logging.debug(f"Start updating the product {product.name}.")

        logging.debug("Validating product information...")
        # Check if price is a number and positive
        if not isinstance(product.price, (int, float)) or product.price <= 0:
            logging.error("Invalid price format. Price must be a positive number.")
            raise InvalidFormatError

        # Check if delivery time is a number and positive
        if not isinstance(product.delivery_time, int) or product.delivery_time <= 0:
            logging.error("Invalid delivery time format. Delivery time must be a positive number.")
            raise InvalidFormatError

        # Check if stock is a number and positive
        if not isinstance(product.stock, int) or product.stock <= 0:
            logging.error("Invalid delivery time format. Stock must be a positive number.")
            raise InvalidFormatError

        logging.debug(f"Checking if product {product_id} exists...")
        existing_product = self.repository.get_by_id(product_id)
        if not existing_product:
            logging.error(f"Product with ID {product_id} does not exist.")
            raise ProductNotExistsError

        logging.debug(f"Updating product {product.name}...")
        product.id = product_id
        updated_product = self.repository.update(product)

        logging.debug(f"Product {product.name} updated successfully.")
        return updated_product
