import logging

from ..domain.entities.product_dto import ProductDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class GetAllProducts:
    """
    Use case for retrieving all products.
    """

    def __init__(self, repository):
        """
        Initializes the GetAllProducts use case with a product repository.
        :param repository:
        """
        self.repository = repository

    def execute(self) -> list[ProductDTO]:
        """
        Retrieves all products from the repository.
        :return: A list of ProductDTO objects.
        """
        logging.debug("Retrieving all products...")
        return self.repository.get_all()
