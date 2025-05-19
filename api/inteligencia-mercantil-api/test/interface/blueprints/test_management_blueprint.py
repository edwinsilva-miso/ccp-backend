import pytest
import json
from unittest.mock import patch, MagicMock

from src.main import create_app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    # Mock the Google Cloud metadata server request
    with patch('requests.get') as mock_get:
        mock_get.return_value.text = "fake-service-account@test.iam.gserviceaccount.com"
        # Mock Google credentials
        with patch('google.auth.default') as mock_default:
            mock_default.return_value = (MagicMock(), "test-project")
            
            app = create_app()
            app.config['TESTING'] = True
            
            with app.test_client() as client:
                # Set up database in test mode
                with app.app_context():
                    yield client


class TestManagementBlueprint:
    def test_health_check(self, client):
        """Test the health check endpoint"""
        # Act
        response = client.get('/health')
        
        # Assert
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['status'] == "OK"
        assert 'timestamp' in result
    
    def test_readiness_check(self, client):
        """Test the readiness check endpoint"""
        # Act
        response = client.get('/readiness')
        
        # Assert
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['status'] == "Ready"
        assert 'timestamp' in result
        
        # Test that database is checked
        assert 'database' in result
        assert result['database']['status'] in ['OK', 'Error']  # Could be either in test context
