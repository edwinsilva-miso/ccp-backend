import logging

from ..domain.entities.order_dto import OrderDTO
from .errors.errors import OrderNotExistsError

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

class GetOrderById:
    """
    Get an order by its ID.
    """

    def __init__(self, order_repository):
        """
        Initializes the GetOrderById with an order repository.
        :param order_repository: An instance of OrderRepository.
        """
        self.order_repository = order_repository

    def execute(self, order_id: str) -> OrderDTO:
        """
        Get an order by its ID.
        :param order_id: The ID of the order to retrieve.
        :return: An OrderDTO object.
        """
        logger.debug(f"Getting order with ID: {order_id}")
        order = self.order_repository.get_order(order_id)
        if not order:
            raise OrderNotExistsError

        logger.debug(f"Order found: {order.to_dict()}")
        return order