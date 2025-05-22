import logging

from ...application.process_orders_message import ProcessOrdersMessage
from ...infrastructure.messaging.rabbitmq_messaging_port_adapter import RabbitMQMessagingPortAdapter
from ...infrastructure.adapters.order_adapter import OrdersAdapter

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

class OrderInitiatedConsumer:
    """
    Interface for the Update Products Stock Consumer.
    """

    def __init__(self):
        order_adapter = OrdersAdapter()
        self.messaging_port = RabbitMQMessagingPortAdapter()
        self.processor = ProcessOrdersMessage(order_adapter)

    def process_message(self, message: dict) -> None:
        """
        Process a message received from the queue.
        :param message: The message received from RabbitMQ
        """
        try:
            self.processor.process(message)
        except Exception as e:
            logging.error(f"Error processing order initiated message: {str(e)}")

    def start_consuming(self) -> None:
        """
        Start consuming messages from the RabbitMQ queue.
        """
        self.messaging_port.consume_messages(
            queue="order_initiated_queue",
            callback=self.process_message,
            exchange="order_initiated_exchange",
            routing_key="order_initiated_routing_key"
        )