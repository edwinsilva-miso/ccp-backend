import pytest
import json
from unittest.mock import patch, MagicMock
from datetime import datetime

from src.interface.blueprints.management_blueprint import get_health_status, get_database_status


class TestManagementFunctions:
    def test_get_health_status(self):
        """Test the get_health_status function"""
        # Act
        result = get_health_status()
        
        # Assert
        assert result['status'] == "OK"
        assert 'timestamp' in result
        # Verify timestamp is a valid ISO format string
        datetime.fromisoformat(result['timestamp'].replace('Z', '+00:00'))
    
    def test_get_database_status_success(self):
        """Test the get_database_status function when database is available"""
        # Arrange
        mock_db = MagicMock()
        
        # Act
        with patch('src.interface.blueprints.management_blueprint.db', mock_db):
            result = get_database_status()
        
        # Assert
        assert result['status'] == "OK"
        mock_db.session.execute.assert_called_once()
    
    def test_get_database_status_error(self):
        """Test the get_database_status function when database has an error"""
        # Arrange
        mock_db = MagicMock()
        mock_db.session.execute.side_effect = Exception("Database connection error")
        
        # Act
        with patch('src.interface.blueprints.management_blueprint.db', mock_db):
            result = get_database_status()
        
        # Assert
        assert result['status'] == "Error"
        assert "Database connection error" in result['message']
        mock_db.session.execute.assert_called_once()
