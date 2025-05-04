import logging

from .errors.errors import OrdersNotFoundError

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class ListOrders:
    """
    Use case for listing orders.
    """

    def __init__(self, order_repository):
        self.order_repository = order_repository

    def execute(self, client_id):
        """
        List all orders for a given client ID.
        :param client_id: The unique identifier of the client whose orders are to be listed.
        :return: A list of orders associated with the client.
        """
        logger.debug("Starting order listing process...")

        # Fetch the orders from the repository
        orders = self.order_repository.get_orders_by_client(client_id)
        if not orders:
            logger.debug(f"No orders found for client {client_id}.")
            raise OrdersNotFoundError

        logger.debug(f"Orders fetched for client {client_id}: {len(orders)} orders found.")
        return orders