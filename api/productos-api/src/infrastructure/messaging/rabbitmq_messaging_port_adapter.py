from typing import Callable

from .rabbitmq_messaging_adapter import RabbitMQMessagingAdapter
from ...domain.ports.messaging_port import MessagingPort


class RabbitMQMessagingPortAdapter(MessagingPort):
    """Implementation of MessagingPort using RabbitMQ"""

    def __init__(self):
        self.adapter = RabbitMQMessagingAdapter()

    def send_message(self, exchange: str, routing_key: str, message: dict) -> bool:
        """Send a message to RabbitMQ"""
        return self.adapter.publish_message(exchange, routing_key, message)

    def consume_messages(self, queue: str, callback: Callable, exchange: str = None,
                         routing_key: str = None) -> None:
        """Set up a consumer for the specified queue"""
        return self.adapter.setup_consumer(
            queue=queue,
            callback=callback,
            exchange=exchange,
            routing_key=routing_key
        )
