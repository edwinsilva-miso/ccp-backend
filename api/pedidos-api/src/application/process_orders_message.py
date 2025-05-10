import logging

from ..domain.entities.order_dto import OrderDTO
from ..domain.entities.order_history_dto import OrderHistoryDTO
from ..domain.entities.order_item_dto import OrderItemDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class ProcessOrdersMessage:
    """
    Process the orders message.
    """

    def __init__(self, order_repository):
        """
        Initializes the ProcessOrdersMessage with an order repository.
        :param order_repository: An instance of OrderRepository.
        """
        self.order_repository = order_repository

    def process(self, message: dict) -> None:
        """
        Process the message.
        """
        # Here you would implement the logic to process the message.
        # For example, updating the stock of products in the database.
        logging.debug(f"Processing message: {message}")
        order = message.get("order")
        order_id = order.get("id")

        # Mapping the order items that compose the original order
        logging.debug("Mapping order items.")
        items = order.get("items", [])
        order_items = []
        for item in items:
            order_item = OrderItemDTO(
                id=item.get("id"),
                order_id=order_id,
                product_id=item.get("productId"),
                quantity=item.get("quantity"),
                unit_price=item.get("unitPrice"),
                total_price=item.get("totalPrice"),
                currency=item.get("currency")
            )
            order_items.append(order_item)

        # Mapping the order history that compose the original order
        logging.debug("Mapping order history.")
        order_history = []
        history = OrderHistoryDTO(
            id=order.get("historyId"),
            order_id=order_id,
            status=order.get("status"),
            description=f"Creación de orden para cliente {order.get('clientId')}",
            date=order.get("historyDate"),

        )
        order_history.append(history)

        order_dto = OrderDTO(
            id=order_id,
            order_date=order.get("orderDate"),
            status=order.get("status"),
            subtotal=order.get("subtotal"),
            taxes=order.get("taxes"),
            total=order.get("total"),
            currency=order.get("currency"),
            client_id=order.get("clientId"),
            payment_id=order.get("paymentId"),
            transaction_status=order.get("transactionStatus"),
            transaction_date=order.get("transactionDate"),
            transaction_id=order.get("transactionId"),
            order_items=order_items,
            order_history=order_history
        )

        # Save the order to the repository
        logging.debug(f"Saving order to repository: {order_dto}")
        self.order_repository.create_order(order_dto)
        logging.debug("Message processed successfully.")
