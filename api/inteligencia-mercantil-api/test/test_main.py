import pytest
from unittest.mock import patch, MagicMock
import os

from src.main import create_app
from src.application.errors.errors import ApiError


@pytest.mark.skip
class TestMain:
    @pytest.fixture
    def mock_google_services(self):
        # Mock Google Cloud metadata server
        with patch('requests.get') as mock_get:
            mock_get.return_value.text = "fake-service-account@test.iam.gserviceaccount.com"
            # Mock Google credentials
            with patch('google.auth.default') as mock_default:
                mock_default.return_value = (MagicMock(), "test-project")
                yield mock_get, mock_default
    
    def test_create_app(self, mock_google_services):
        """Test that the application can be created successfully"""
        # Set required environment variables
        os.environ['DB_USER'] = 'test_user'
        os.environ['DB_PASSWORD'] = 'test_password'
        os.environ['DB_HOST'] = 'localhost'
        os.environ['DB_PORT'] = '5432'
        os.environ['DB_NAME'] = 'test_db'
        
        # Act
        app = create_app()
        
        # Assert
        assert app is not None
        assert len(app.blueprints) > 0
        assert 'management' in app.blueprints
        assert 'video' in app.blueprints
    
    def test_error_handler(self, mock_google_services):
        """Test that the API error handler works correctly"""
        # Arrange
        os.environ['DB_USER'] = 'test_user'
        os.environ['DB_PASSWORD'] = 'test_password'
        os.environ['DB_HOST'] = 'localhost'
        os.environ['DB_PORT'] = '5432'
        os.environ['DB_NAME'] = 'test_db'
        
        app = create_app()
        app.config['TESTING'] = True
        
        # Create a test endpoint that raises an ApiError
        @app.route('/test-error')
        def test_error():
            raise ApiError("Test error message", code=422)
        
        # Act
        with app.test_client() as client:
            response = client.get('/test-error')
        
        # Assert
        assert response.status_code == 422
        assert response.json['msg'] == "Test error message"
    
    def test_app_run(self, mock_google_services):
        """Test that the app can be run with default port"""
        # Arrange
        os.environ['DB_USER'] = 'test_user'
        os.environ['DB_PASSWORD'] = 'test_password'
        os.environ['DB_HOST'] = 'localhost'
        os.environ['DB_PORT'] = '5432'
        os.environ['DB_NAME'] = 'test_db'
        
        # Act/Assert
        with patch('src.main.Flask.run') as mock_run:
            # Remove PORT environment variable to test default
            os.environ.pop('PORT', None)
            
            # Import __name__ == "__main__" code
            import importlib
            with patch.object(importlib.import_module('src.main'), '__name__', '__main__'):
                importlib.reload(importlib.import_module('src.main'))
            
            # Verify run was called with expected args
            mock_run.assert_called_once_with(host="0.0.0.0", port=5000, debug=True)
