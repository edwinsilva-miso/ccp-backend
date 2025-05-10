import json
import logging
import threading
from contextlib import contextmanager

import pika

from .rabbitmq_connection_manager import RabbitMQConnectionManager


class RabbitMQMessagingAdapter:
    """Adapter for sending messages to RabbitMQ"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.connection_manager = RabbitMQConnectionManager()

    @contextmanager
    def _channel(self):
        """Context manager for getting and returning connections"""
        connection = self.connection_manager.get_connection()
        channel = connection.channel()
        try:
            yield channel
        finally:
            channel.close()
            self.connection_manager.return_connection(connection)

    def publish_message(self, exchange, routing_key, message, exchange_type='direct'):
        """Publish a message to RabbitMQ"""
        self.logger.debug(f"Publishing message to {exchange} with routing key {routing_key}")

        try:
            with self._channel() as channel:
                # Declare exchange
                channel.exchange_declare(
                    exchange=exchange,
                    exchange_type=exchange_type,
                    durable=True
                )

                # Publish message
                channel.basic_publish(
                    exchange=exchange,
                    routing_key=routing_key,
                    body=json.dumps(message),
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # Make message persistent
                        content_type='application/json'
                    )
                )
                self.logger.debug(f"Message published successfully")
                return True
        except Exception as e:
            self.logger.error(f"Failed to publish message: {str(e)}")
            return False

    def setup_consumer(self, queue, callback, exchange=None, routing_key=None, exchange_type='direct'):
        """
        Set up a consumer for a queue with the given callback

        Args:
            queue: Queue name to consume from
            callback: Function to process received messages
            exchange: Optional exchange to bind the queue to
            routing_key: Optional routing key for binding
            exchange_type: Type of exchange if creating
        """

        def consumer_thread():
            try:
                connection = self.connection_manager.get_connection()
                channel = connection.channel()

                # Declare queue
                channel.queue_declare(queue=queue, durable=True)

                # If exchange provided, declare and bind
                if exchange and routing_key:
                    channel.exchange_declare(
                        exchange=exchange,
                        exchange_type=exchange_type,
                        durable=True
                    )
                    channel.queue_bind(
                        queue=queue,
                        exchange=exchange,
                        routing_key=routing_key
                    )

                # Create wrapper for the callback to handle JSON parsing
                def process_message(ch, method, properties, body):
                    try:
                        message = json.loads(body)
                        callback(message)
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                    except Exception as e:
                        self.logger.error(f"Error processing message: {str(e)}")
                        # Negative acknowledgment, message will be requeued
                        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

                # Set prefetch count to control concurrency
                channel.basic_qos(prefetch_count=1)

                # Start consuming
                channel.basic_consume(queue=queue, on_message_callback=process_message)

                self.logger.info(f"Started consuming from queue: {queue}")
                channel.start_consuming()

            except Exception as e:
                self.logger.error(f"Consumer error: {str(e)}")
                # Sleep briefly before reconnection attempt
                import time
                time.sleep(5)

                # Try to restart the consumer
                self.logger.info("Attempting to restart consumer...")
                consumer_thread()
            finally:
                if 'connection' in locals() and connection.is_open:
                    self.connection_manager.return_connection(connection)

        # Start consumer in a separate thread
        thread = threading.Thread(target=consumer_thread, daemon=True)
        thread.start()
        return thread
