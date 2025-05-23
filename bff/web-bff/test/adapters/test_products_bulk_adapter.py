import io
import unittest
from unittest.mock import patch, MagicMock

# Fix the import by using a relative import or adjusting your PYTHONPATH
# Option 1: If src is at the same level as test
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.adapters.products_bulk_adapter import ProductsBulkAdapter


class TestProductsBulkAdapter(unittest.TestCase):

    def setUp(self):
        self.adapter = ProductsBulkAdapter()
        self.csv_content = "name,price,description\nProduct1,10.99,Test description\nProduct2,20.99,Another description"

    # Mock the RabbitMQ connection to prevent AMQPConnectionError
    @patch('pika.BlockingConnection')
    @patch('src.adapters.products_bulk_adapter.ProductsBulkProducer')
    def test_process_file_success(self, mock_producer_class, mock_connection):
        # Arrange
        mock_producer = MagicMock()
        mock_producer_class.return_value = mock_producer

        mock_file = MagicMock()
        mock_file.stream = io.BytesIO(self.csv_content.encode('utf-8'))

        # Act
        result = self.adapter.process_file(mock_file)

        # Assert
        self.assertEqual(result["message"], "File successfully uploaded and processed")
        self.assertEqual(result["productsToProcessed"], "2 products")

    @patch('pika.BlockingConnection')
    @patch('src.adapters.products_bulk_adapter.ProductsBulkProducer')
    def test_process_file_exceeds_max_size(self, mock_producer_class, mock_connection):
        # Arrange
        mock_producer = MagicMock()
        mock_producer_class.return_value = mock_producer

        mock_file = MagicMock()
        mock_file.stream = MagicMock()
        # Mock a file larger than 50MB
        mock_file.stream.tell.return_value = 51 * 1024 * 1024

        # Act
        result = self.adapter.process_file(mock_file)

        # Assert
        self.assertEqual(result["msg"], "File size exceeds the maximum limit of 50MB")
        mock_producer.produce.assert_not_called()

    @patch('pika.BlockingConnection')
    @patch('src.adapters.products_bulk_adapter.ProductsBulkProducer')
    @patch('src.adapters.products_bulk_adapter.csv.DictReader')
    def test_process_file_empty_csv(self, mock_dict_reader, mock_producer_class, mock_connection):
        # Arrange
        mock_producer = MagicMock()
        mock_producer_class.return_value = mock_producer

        mock_file = MagicMock()
        mock_file.stream = io.BytesIO("name,price,description".encode('utf-8'))

        # Mock empty CSV (no rows)
        mock_dict_reader.return_value = []

        # Act
        result = self.adapter.process_file(mock_file)

        # Assert
        self.assertEqual(result["message"], "File successfully uploaded and processed")
        self.assertEqual(result["productsToProcessed"], "0 products")
        mock_producer.produce.assert_not_called()

    @patch('pika.BlockingConnection')
    @patch('src.adapters.products_bulk_adapter.ProductsBulkProducer')
    @patch('src.adapters.products_bulk_adapter.logger')
    def test_process_file_logs_debug_messages(self, mock_logger, mock_producer_class, mock_connection):
        # Arrange
        mock_producer = MagicMock()
        mock_producer_class.return_value = mock_producer

        mock_file = MagicMock()
        mock_file.stream = io.BytesIO(self.csv_content.encode('utf-8'))

        # Act
        self.adapter.process_file(mock_file)

        # Assert
        # Verify debug logs were called
        mock_logger.debug.assert_any_call("Beginning file processing...")
        mock_logger.debug.assert_any_call("Reading the CSV file...")
        mock_logger.debug.assert_any_call("Processing the products...")
        mock_logger.debug.assert_any_call("Finished processing the file")