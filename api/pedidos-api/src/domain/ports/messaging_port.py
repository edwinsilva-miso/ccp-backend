# src/domain/ports/messaging_port.py
from abc import ABC, abstractmethod
from typing import Callable


class MessagingPort(ABC):
    """Port for messaging services"""

    @abstractmethod
    def send_message(self, exchange: str, routing_key: str, message: dict) -> bool:
        """
        Send a message to the message broker

        Args:
            exchange: The exchange to publish to
            routing_key: The routing key for the message
            message: The message payload

        Returns:
            bool: True if message was sent successfully
        """
        pass

    @abstractmethod
    def consume_messages(self, queue: str, callback: Callable, exchange: str = None,
                         routing_key: str = None) -> None:
        """
        Set up a consumer to process messages from a queue

        Args:
            queue: The queue to consume from
            callback: Function to call when a message is received
            exchange: Optional exchange to bind the queue to
            routing_key: Optional routing key for the binding
        """
        pass
