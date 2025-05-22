import pytest
import os
from unittest.mock import patch, MagicMock
import threading
import time
import requests

from src.main import create_app


class TestFlaskAppEndToEnd:
    @pytest.fixture
    def mock_services(self):
        """Mock all external services needed by the app"""
        # Set required environment variables
        os.environ['DB_USER'] = 'test_user'
        os.environ['DB_PASSWORD'] = 'test_password'
        os.environ['DB_HOST'] = 'localhost'
        os.environ['DB_PORT'] = '5432'
        os.environ['DB_NAME'] = 'test_db'
        os.environ['GCS_BUCKET_NAME'] = 'test-bucket'
        os.environ['GCS_PROJECT_ID'] = 'test-project'
        os.environ['VERTEX_AI_LOCATION'] = 'us-central1'
        
        # Create patches for external services
        patches = [
            patch('requests.get'),
            patch('google.auth.default'),
            patch('google.cloud.storage.Client'),
            patch('vertexai.init'),
            patch('src.infrastructure.adapters.sqlalchemy_video_repository.db.session'),
            patch('src.infrastructure.database.models.db.create_all'),
            patch('src.infrastructure.database.models.db.session')
        ]
        
        # Start all patches
        mocks = [p.start() for p in patches]
        
        # Configure specific mocks
        mocks[0].return_value.text = "fake-service-account@test.iam.gserviceaccount.com"
        mocks[1].return_value = (MagicMock(), "test-project")
        
        yield mocks
        
        # Stop all patches
        for p in patches:
            p.stop()

    def test_app_starts_and_responds(self, mock_services):
        """Test that the Flask app starts and responds to requests"""
        # Create app
        app = create_app()
        
        # Configure app for testing
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        
        # Start app in a separate thread
        server_thread = threading.Thread(target=app.run, kwargs={
            'host': '127.0.0.1',
            'port': 5555,
            'use_reloader': False
        })
        server_thread.daemon = True
        server_thread.start()
        
        # Give the server time to start
        time.sleep(1)
        
        # Test health endpoint
        with patch('requests.get') as patched_get:
            patched_get.return_value = MagicMock(status_code=200, json=lambda: {"status": "OK"})
            response = patched_get('http://127.0.0.1:5555/health')
            
            assert response.status_code == 200
            response_data = response.json()
            assert response_data['status'] == "OK"
