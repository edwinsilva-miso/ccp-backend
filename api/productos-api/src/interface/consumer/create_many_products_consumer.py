import logging

from ...application.create_many_products import CreateManyProducts
from ...infrastructure.messaging.rabbitmq_messaging_port_adapter import RabbitMQMessagingPortAdapter
from ...infrastructure.adapters.product_adapter import ProductAdapter

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

class CreateManyProductsConsumer:
    """
    Interface for the Create Many Products Consumer.
    """

    def __init__(self):
        products_adapter = ProductAdapter()
        self.messaging_port = RabbitMQMessagingPortAdapter()
        self.processor = CreateManyProducts(products_adapter)

    def process_message(self, message: dict) -> None:
        """
        Process a message received from the queue.
        :param message: The message received from RabbitMQ
        """
        try:
            self.processor.process(message)
        except Exception as e:
            logging.error(f"Error processing creating many products: {str(e)}")

    def start_consuming(self) -> None:
        """
        Start consuming messages from the RabbitMQ queue.
        """
        self.messaging_port.consume_messages(
            queue="create_multiple_products_queue",
            callback=self.process_message,
            exchange="create_multiple_products_exchange",
            routing_key="create_multiple_products_routing_key"
        )