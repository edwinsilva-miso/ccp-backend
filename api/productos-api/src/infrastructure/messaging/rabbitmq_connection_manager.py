import logging
import os
import time

from pika.adapters.blocking_connection import BlockingConnection
from pika.connection import ConnectionParameters
from pika.credentials import PlainCredentials


class RabbitMQConnectionManager:
    """Manages RabbitMQ connections with connection pooling and retry logic"""

    def __init__(self, pool_size=5, max_retries=30, retry_delay=5):
        self.logger = logging.getLogger(__name__)
        self.pool_size = pool_size
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.connection_pool = []

        # Get connection parameters from environment
        self.host = os.environ.get('RABBITMQ_HOST', 'localhost')
        self.port = int(os.environ.get('RABBITMQ_PORT', 5672))
        self.user = os.environ.get('RABBITMQ_USER', 'admin')
        self.password = os.environ.get('RABBITMQ_PASSWORD', 'admin')

        self.logger.info(f"Connecting to RabbitMQ at {self.host}:{self.port}")

        self.credentials = PlainCredentials(self.user, self.password)
        self.parameters = ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=self.credentials,
            heartbeat=600,
            # Add retry settings at connection parameter level
            connection_attempts=3,
            retry_delay=2
        )

        # Initialize pool with retry logic
        self._initialize_pool_with_retry()

    def _initialize_pool_with_retry(self):
        """Initialize the connection pool with retry logic"""
        self.logger.info(f"Initializing RabbitMQ connection pool with retry logic")

        retries = 0
        while retries < self.max_retries and len(self.connection_pool) < self.pool_size:
            try:
                # Create initial connection to test connectivity
                if not self.connection_pool:
                    self.logger.info(
                        f"Attempt {retries + 1}/{self.max_retries} to connect to RabbitMQ at {self.host}:{self.port}")
                    connection = BlockingConnection(self.parameters)
                    self.connection_pool.append(connection)
                    self.logger.info("Successfully connected to RabbitMQ")

                # Fill the rest of the pool
                while len(self.connection_pool) < self.pool_size:
                    connection = BlockingConnection(self.parameters)
                    self.connection_pool.append(connection)

                self.logger.info(f"Connection pool initialized with {len(self.connection_pool)} connections")
                return

            except Exception as e:
                retries += 1
                self.logger.warning(f"Failed to connect to RabbitMQ (attempt {retries}/{self.max_retries}): {str(e)}")

                # Wait before retrying
                if retries < self.max_retries:
                    self.logger.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)

        if not self.connection_pool:
            self.logger.error(f"Failed to initialize connection pool after {self.max_retries} attempts")

    def get_connection(self):
        """Get a connection from the pool or create a new one if needed"""
        # Try to establish connection if pool is empty
        if not self.connection_pool:
            self.logger.warning("Connection pool empty, attempting to create new connection")
            try:
                return BlockingConnection(self.parameters)
            except Exception as e:
                self.logger.error(f"Failed to create RabbitMQ connection: {str(e)}")
                raise

        connection = self.connection_pool.pop()
        if not connection.is_open:
            self.logger.info("Connection closed, creating new one")
            try:
                connection = BlockingConnection(self.parameters)
            except Exception as e:
                self.logger.error(f"Failed to create RabbitMQ connection: {str(e)}")
                raise

        return connection

    def return_connection(self, connection):
        """Return a connection to the pool"""
        if connection and connection.is_open:
            self.connection_pool.append(connection)
        else:
            self.logger.info("Connection closed, not returning to pool")

    def close_all(self):
        """Close all connections in the pool"""
        for connection in self.connection_pool:
            if connection and connection.is_open:
                try:
                    connection.close()
                except Exception as e:
                    self.logger.warning(f"Error closing connection: {str(e)}")
        self.connection_pool = []