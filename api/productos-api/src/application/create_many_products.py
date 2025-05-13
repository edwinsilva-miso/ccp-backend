import logging

from ..domain.mapper.products_json_mapper import ProductsJsonMapper

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class CreateManyProducts:
    """
    Use case for creating multiple products.
    """

    def __init__(self, repository):
        """
        Initializes the CreateManyProducts use case with a product repository.
        :param repository:
        """
        self.repository = repository

    def process(self, message: dict) -> None:
        """
        Executes the creation of multiple products.
        :param message: The message containing the products to be created.
        """
        logging.debug("Begin creating multiple products...")
        logging.debug(f"Converting message to product list {message}...")
        product_list = ProductsJsonMapper.from_json_to_dto_list(message)
        if not product_list:
            logging.error("No products found in the message.")
            return
        logging.debug(f"Creating {len(product_list)} products...")
        self.repository.add_all(product_list)
        logging.debug("End creating multiple products...")
