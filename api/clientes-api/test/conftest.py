import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from dotenv import load_dotenv

os.environ['ENV'] = 'test'


def pytest_configure(config):
    root = Path(__file__).parent.parent
    env_path = root / '.env.test'
    load_dotenv(str(env_path))
    return config


@pytest.fixture(autouse=True)
def mock_rabbitmq_client():
    """Mock your custom RabbitMQ client if you have one"""
    # Adjust the path to match your actual client class
    with patch('src.infrastructure.messaging.rabbitmq_connection_manager.RabbitMQConnectionManager') as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        mock_instance.send_message.return_value = None
        mock_instance.connect.return_value = None
        yield


@pytest.fixture(autouse=True)
def mock_rabbitmq_producer():
    """
    Mock all possible RabbitMQ connection paths to prevent any connection attempts.
    """
    # Common import paths for pika's BlockingConnection
    with patch('pika.BlockingConnection') as mock_connection_class, \
            patch('pika.adapters.blocking_connection.BlockingConnection') as mock_adapter_connection:
        # Create mock objects
        mock_connection = MagicMock()
        mock_channel = MagicMock()

        # Configure both connection mocks
        for conn in [mock_connection_class, mock_adapter_connection]:
            conn.return_value = mock_connection

        mock_connection.channel.return_value = mock_channel
        mock_connection.is_open = True
        mock_channel.basic_publish.return_value = True

        # Additional mocks for connection parameters
        with patch('pika.ConnectionParameters') as mock_params:
            mock_params.return_value = MagicMock()
            yield


@pytest.fixture(autouse=True)
def mock_google_credentials():
    """Mock Google Cloud credentials to avoid authentication errors in CI"""
    credentials_mock = MagicMock()
    credentials_mock.universe_domain = "googleapis.com"

    with patch('google.auth.default', return_value=(credentials_mock, 'project')):
        yield