import logging

from ..domain.entities.order_dto import OrderDTO
from .errors.errors import OrdersNotFoundError

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

class ListsOrders:
    """
    Lists all orders.
    """

    def __init__(self, order_repository):
        """
        Initializes the ListsOrders with an order repository.
        :param order_repository: An instance of OrderRepository.
        """
        self.order_repository = order_repository

    def execute(self) -> list[OrderDTO]:
        """
        List all orders.
        :return: A list of OrderDTO objects.
        """
        logger.debug("Listing all orders.")
        orders = self.order_repository.list_orders()
        if not orders:
            raise OrdersNotFoundError("No orders found.")

        logger.debug(f"Orders found: {len(orders)}")
        return orders