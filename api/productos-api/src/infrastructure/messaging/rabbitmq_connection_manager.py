import logging
import os

from pika.adapters.blocking_connection import BlockingConnection
from pika.connection import ConnectionParameters
from pika.credentials import PlainCredentials


class RabbitMQConnectionManager:
    """Manages RabbitMQ connections with connection pooling"""

    def __init__(self, pool_size=5):
        self.logger = logging.getLogger(__name__)
        self.pool_size = pool_size
        self.connection_pool = []
        self.credentials = PlainCredentials(
            os.environ.get('RABBITMQ_USER', 'admin'),
            os.environ.get('RABBITMQ_PASSWORD', 'admin')
        )
        self.parameters = ConnectionParameters(
            host=os.environ.get('RABBITMQ_HOST', 'localhost'),
            port=int(os.environ.get('RABBITMQ_PORT', 5672)),
            credentials=self.credentials,
            heartbeat=600
        )
        self._initialize_pool()

    def _initialize_pool(self):
        """Initialize the connection pool with the specified size"""
        self.logger.info(f"Initializing RabbitMQ connection pool with {self.pool_size} connections")
        for _ in range(self.pool_size):
            try:
                connection = BlockingConnection(self.parameters)
                self.connection_pool.append(connection)
            except Exception as e:
                self.logger.error(f"Failed to create RabbitMQ connection: {str(e)}")

    def get_connection(self):
        """Get a connection from the pool or create a new one if needed"""
        if not self.connection_pool:
            self.logger.warning("Connection pool empty, creating new connection")
            return BlockingConnection(self.parameters)

        connection = self.connection_pool.pop()
        if not connection.is_open:
            self.logger.info("Connection closed, creating new one")
            connection = BlockingConnection(self.parameters)
        return connection

    def return_connection(self, connection):
        """Return a connection to the pool"""
        if connection.is_open:
            self.connection_pool.append(connection)
        else:
            self.logger.info("Connection closed, not returning to pool")

    def close_all(self):
        """Close all connections in the pool"""
        for connection in self.connection_pool:
            if connection.is_open:
                connection.close()
        self.connection_pool = []
