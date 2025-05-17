import pytest
from unittest.mock import MagicMock, patch

from src.infrastructure.dao.warehouse_dao import WarehouseDAO
from src.infrastructure.model.warehouse_model import WarehouseModel


class TestWarehouseDAO:
    """Test suite for WarehouseDAO"""

    @patch('src.infrastructure.dao.warehouse_dao.Session')
    def test_save(self, mock_session_class):
        """Test save method"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        warehouse = MagicMock(spec=WarehouseModel)

        # Act
        result = WarehouseDAO.save(warehouse)

        # Assert
        mock_session.add.assert_called_once_with(warehouse)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(warehouse)
        mock_session.close.assert_called_once()
        assert result == warehouse

    @patch('src.infrastructure.dao.warehouse_dao.Session')
    def test_update(self, mock_session_class):
        """Test update method"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        warehouse = MagicMock(spec=WarehouseModel)
        merged_warehouse = MagicMock(spec=WarehouseModel)
        mock_session.merge.return_value = merged_warehouse

        # Act
        result = WarehouseDAO.update(warehouse)

        # Assert
        mock_session.merge.assert_called_once_with(warehouse)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(merged_warehouse)
        mock_session.close.assert_called_once()
        assert result == merged_warehouse

    @patch('src.infrastructure.dao.warehouse_dao.Session')
    def test_delete_success(self, mock_session_class):
        """Test delete method when warehouse exists"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        warehouse_id = "w123"
        mock_warehouse = MagicMock(spec=WarehouseModel)
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_warehouse

        # Act
        result = WarehouseDAO.delete(warehouse_id)

        # Assert
        mock_session.query.assert_called_once_with(WarehouseModel)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        mock_session.delete.assert_called_once_with(mock_warehouse)
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()
        assert result is True

    @patch('src.infrastructure.dao.warehouse_dao.Session')
    def test_delete_not_found(self, mock_session_class):
        """Test delete method when warehouse does not exist"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        warehouse_id = "nonexistent"
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None

        # Act
        result = WarehouseDAO.delete(warehouse_id)

        # Assert
        mock_session.query.assert_called_once_with(WarehouseModel)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()
        mock_session.close.assert_called_once()
        assert result is False

    @patch('src.infrastructure.dao.warehouse_dao.Session')
    def test_get_by_id_found(self, mock_session_class):
        """Test get_by_id method when warehouse exists"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        warehouse_id = "w123"
        mock_warehouse = MagicMock(spec=WarehouseModel)
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_warehouse

        # Act
        result = WarehouseDAO.get_by_id(warehouse_id)

        # Assert
        mock_session.query.assert_called_once_with(WarehouseModel)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        mock_session.close.assert_called_once()
        assert result == mock_warehouse

    @patch('src.infrastructure.dao.warehouse_dao.Session')
    def test_get_by_id_not_found(self, mock_session_class):
        """Test get_by_id method when warehouse does not exist"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        warehouse_id = "nonexistent"
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None

        # Act
        result = WarehouseDAO.get_by_id(warehouse_id)

        # Assert
        mock_session.query.assert_called_once_with(WarehouseModel)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        mock_session.close.assert_called_once()
        assert result is None

    @patch('src.infrastructure.dao.warehouse_dao.Session')
    def test_get_all(self, mock_session_class):
        """Test get_all method"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_warehouses = [MagicMock(spec=WarehouseModel), MagicMock(spec=WarehouseModel)]
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.all.return_value = mock_warehouses

        # Act
        result = WarehouseDAO.get_all()

        # Assert
        mock_session.query.assert_called_once_with(WarehouseModel)
        mock_query.all.assert_called_once()
        mock_session.close.assert_called_once()
        assert result == mock_warehouses

    @patch('src.infrastructure.dao.warehouse_dao.Session')
    def test_get_by_administrator_id(self, mock_session_class):
        """Test get_by_administrator_id method"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        administrator_id = "admin123"
        mock_warehouses = [MagicMock(spec=WarehouseModel), MagicMock(spec=WarehouseModel)]
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.all.return_value = mock_warehouses

        # Act
        result = WarehouseDAO.get_by_administrator_id(administrator_id)

        # Assert
        mock_session.query.assert_called_once_with(WarehouseModel)
        mock_query.filter.assert_called_once()
        mock_filter.all.assert_called_once()
        mock_session.close.assert_called_once()
        assert result == mock_warehouses