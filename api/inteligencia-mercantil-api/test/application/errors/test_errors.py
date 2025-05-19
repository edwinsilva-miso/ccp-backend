import pytest

from src.application.errors.errors import ApiError


class TestApiError:
    def test_init_with_defaults(self):
        """Test that ApiError can be initialized with defaults"""
        # Act
        error = ApiError("Test error")
        
        # Assert
        assert error.description == "Test error"
        assert error.code == 500  # Default status code
    
    def test_init_with_custom_code(self):
        """Test that ApiError can be initialized with a custom code"""
        # Act
        error = ApiError("Not found", code=404)
        
        # Assert
        assert error.description == "Not found"
        assert error.code == 404
    
    def test_str_representation(self):
        """Test the string representation of ApiError"""
        # Act
        error = ApiError("Bad request", code=400)
        
        # Assert
        # Check that the string representation includes the error details
        assert str(error) == "ApiError: Bad request (400)"
