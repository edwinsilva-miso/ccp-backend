"""
Pytest configuration file for the project.
"""
import os
import pytest
from unittest.mock import patch


def pytest_configure(config):
    """Configure pytest environment variables and settings"""
    os.environ['TESTING'] = 'True'
    

@pytest.fixture(autouse=True)
def mock_env_variables():
    """Set environment variables for all tests"""
    with patch.dict('os.environ', {
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_password',
        'DB_HOST': 'localhost',
        'DB_PORT': '5432',
        'DB_NAME': 'test_db',
        'GCS_BUCKET_NAME': 'test-bucket',
        'GCS_PROJECT_ID': 'test-project',
        'VERTEX_AI_LOCATION': 'us-central1'
    }):
        yield
