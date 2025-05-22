import logging

from ..domain.entities.order_dto import OrderDTO
from .errors.errors import OrderNotExistsError

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

class GetOrderBySalesmanId:
    """
    Use case for getting an order by its ID.
    """

    def __init__(self, order_repository):
        self.order_repository = order_repository

    def execute(self, salesman_id: str) -> list[OrderDTO]:
        """
        Get an order by its ID.
        :param salesman_id : The unique identifier of the salesman whose orders are to be retrieved.
        :return: The order associated with the given ID.
        """
        logger.debug("Starting process to get order by salesman...")

        # Fetch the order from the repository
        order = self.order_repository.get_orders_by_salesman(salesman_id)
        if not order:
            logger.debug(f"Order associated to salesman {salesman_id} not found.")
            raise OrderNotExistsError

        logger.debug(f"Order fetched successfully: {order}")
        return order