import logging

from ...application.process_update_products_stock_message import ProcessUpdateProductsStockMessage
from ...infrastructure.messaging.rabbitmq_messaging_port_adapter import RabbitMQMessagingPortAdapter

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

class UpdateProductsStockConsumer:
    """
    Interface for the Update Products Stock Consumer.
    """

    def __init__(self):
        self.messaging_port = RabbitMQMessagingPortAdapter()
        self.processor = ProcessUpdateProductsStockMessage()

    def process_message(self, message: dict) -> None:
        """
        Process a message received from the queue.
        :param message: The message received from RabbitMQ
        """
        try:
            self.processor.process(message)
        except Exception as e:
            logging.error(f"Error processing stock update message: {str(e)}")

    def start_consuming(self) -> None:
        """
        Start consuming messages from the RabbitMQ queue.
        """
        self.messaging_port.consume_messages(
            queue="update_stock_queue",
            callback=self.process_message,
            exchange="update_stock_exchange",
            routing_key="update_stock_routing_key"
        )