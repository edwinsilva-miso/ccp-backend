import pytest
import json
from unittest.mock import patch, MagicMock

from src.main import create_app
from src.application.errors.errors import ApiError

class TestErrorHandling:
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        # Mock the Google Cloud metadata server request
        with patch('requests.get') as mock_get:
            mock_get.return_value.text = "fake-service-account@test.iam.gserviceaccount.com"
            # Mock Google credentials
            with patch('google.auth.default') as mock_default:
                mock_default.return_value = (MagicMock(), "test-project")
                
                # Set required environment variables
                with patch.dict('os.environ', {
                    'DB_USER': 'test_user',
                    'DB_PASSWORD': 'test_password',
                    'DB_HOST': 'localhost',
                    'DB_PORT': '5432',
                    'DB_NAME': 'test_db'
                }):
                    app = create_app()
                    app.config['TESTING'] = True
                    
                    # Add a test route that raises different API errors
                    @app.route('/test-error/<int:code>')
                    def test_error(code):
                        raise ApiError(f"Test error with code {code}", code=code)
                    
                    with app.test_client() as client:
                        yield client
    
    def test_400_error(self, client):
        """Test handling of 400 Bad Request errors"""
        # Act
        response = client.get('/test-error/400')
        
        # Assert
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['msg'] == "Test error with code 400"
    
    def test_404_error(self, client):
        """Test handling of 404 Not Found errors"""
        # Act
        response = client.get('/test-error/404')
        
        # Assert
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['msg'] == "Test error with code 404"
    
    def test_500_error(self, client):
        """Test handling of 500 Internal Server Error"""
        # Act
        response = client.get('/test-error/500')
        
        # Assert
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['msg'] == "Test error with code 500"
