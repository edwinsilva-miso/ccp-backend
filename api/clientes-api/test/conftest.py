import os
import pytest
from pathlib import Path

from dotenv import load_dotenv

os.environ['ENV'] = 'test'


def pytest_configure(config):
    root = Path(__file__).parent.parent
    env_path = root / '.env.test'
    load_dotenv(str(env_path))
    return config


@pytest.fixture
def mock_rabbitmq(monkeypatch):
    """Mock RabbitMQ connection to prevent delays in tests"""

    def mock_publish(*args, **kwargs):
        return True

    monkeypatch.setattr('your_module.publish_message', mock_publish)
