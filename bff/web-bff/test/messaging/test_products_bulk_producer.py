import json
import unittest
from unittest.mock import patch, MagicMock

from src.messaging.producer.products_bulk_producer import ProductsBulkProducer


class TestProductsBulkProducer(unittest.TestCase):

    @patch('src.messaging.producer.products_bulk_producer.pika.BlockingConnection')
    def test_produce_message_successfully(self, mock_connection):
        # Arrange
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        test_message = {"products": [{"name": "Test Product", "price": 10.99}]}

        # Act
        ProductsBulkProducer.produce(test_message)

        # Assert
        mock_connection.assert_called_once()
        mock_channel.queue_declare.assert_called_once_with(queue='create_multiple_products_queue', durable=True)
        mock_channel.basic_publish.assert_called_once()

        # Check that basic_publish was called with the correct arguments
        call_args = mock_channel.basic_publish.call_args[1]
        self.assertEqual(call_args['exchange'], 'create_multiple_products_exchange')
        self.assertEqual(call_args['routing_key'], 'create_multiple_products_routing_key')
        self.assertEqual(call_args['body'], json.dumps(test_message))

        # Verify connection was closed
        mock_connection.return_value.close.assert_called_once()

    @patch('src.messaging.producer.products_bulk_producer.pika.BlockingConnection')
    @patch('src.messaging.producer.products_bulk_producer.logger')
    def test_produce_logs_message_sent(self, mock_logger, mock_connection):
        # Arrange
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        test_message = {"products": [{"name": "Test Product", "price": 10.99}]}

        # Act
        ProductsBulkProducer.produce(test_message)

        # Assert
        mock_logger.info.assert_called_once_with('<< Message sent to queue')

    @patch('src.messaging.producer.products_bulk_producer.pika.BlockingConnection')
    def test_produce_connection_parameters(self, mock_connection):
        # Arrange
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        test_message = {"products": [{"name": "Test Product"}]}

        # Act
        ProductsBulkProducer.produce(test_message)

        # Assert
        # Verify that ConnectionParameters was called with the right environment variables
        connection_params_call = mock_connection.call_args[0][0]
        self.assertEqual(connection_params_call.host, 'localhost')
        self.assertEqual(connection_params_call.port, 5672)