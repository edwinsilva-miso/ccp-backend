import pytest
from unittest.mock import MagicMock, patch

from src.infrastructure.dao.warehouse_stock_item_dao import WarehouseStockItemDAO
from src.infrastructure.model.warehouse_stock_item_model import WarehouseStockItemModel


class TestWarehouseStockItemDAO:
    """Test suite for WarehouseStockItemDAO"""

    @patch('src.infrastructure.dao.warehouse_stock_item_dao.Session')
    def test_save(self, mock_session_class):
        """Test save method"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        stock_item = MagicMock(spec=WarehouseStockItemModel)

        # Act
        result = WarehouseStockItemDAO.save(stock_item)

        # Assert
        mock_session.add.assert_called_once_with(stock_item)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(stock_item)
        mock_session.close.assert_called_once()
        assert result == stock_item

    @patch('src.infrastructure.dao.warehouse_stock_item_dao.Session')
    def test_update(self, mock_session_class):
        """Test update method"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        stock_item = MagicMock(spec=WarehouseStockItemModel)
        merged_item = MagicMock(spec=WarehouseStockItemModel)
        mock_session.merge.return_value = merged_item

        # Act
        result = WarehouseStockItemDAO.update(stock_item)

        # Assert
        mock_session.merge.assert_called_once_with(stock_item)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(merged_item)
        mock_session.close.assert_called_once()
        assert result == merged_item

    @patch('src.infrastructure.dao.warehouse_stock_item_dao.Session')
    def test_delete_success(self, mock_session_class):
        """Test delete method when stock item exists"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        item_id = "wsi123"
        mock_stock_item = MagicMock(spec=WarehouseStockItemModel)
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_stock_item

        # Act
        result = WarehouseStockItemDAO.delete(item_id)

        # Assert
        mock_session.query.assert_called_once_with(WarehouseStockItemModel)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        mock_session.delete.assert_called_once_with(mock_stock_item)
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()
        assert result is True

    @patch('src.infrastructure.dao.warehouse_stock_item_dao.Session')
    def test_delete_not_found(self, mock_session_class):
        """Test delete method when stock item does not exist"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        item_id = "nonexistent"
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None

        # Act
        result = WarehouseStockItemDAO.delete(item_id)

        # Assert
        mock_session.query.assert_called_once_with(WarehouseStockItemModel)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()
        mock_session.close.assert_called_once()
        assert result is False

    @patch('src.infrastructure.dao.warehouse_stock_item_dao.Session')
    def test_get_by_id_found(self, mock_session_class):
        """Test get_by_id method when stock item exists"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        item_id = "wsi123"
        mock_stock_item = MagicMock(spec=WarehouseStockItemModel)
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_stock_item

        # Act
        result = WarehouseStockItemDAO.get_by_id(item_id)

        # Assert
        mock_session.query.assert_called_once_with(WarehouseStockItemModel)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        mock_session.close.assert_called_once()
        assert result == mock_stock_item

    @patch('src.infrastructure.dao.warehouse_stock_item_dao.Session')
    def test_get_by_id_not_found(self, mock_session_class):
        """Test get_by_id method when stock item does not exist"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        item_id = "nonexistent"
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None

        # Act
        result = WarehouseStockItemDAO.get_by_id(item_id)

        # Assert
        mock_session.query.assert_called_once_with(WarehouseStockItemModel)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        mock_session.close.assert_called_once()
        assert result is None

    @patch('src.infrastructure.dao.warehouse_stock_item_dao.Session')
    def test_get_all(self, mock_session_class):
        """Test get_all method"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_stock_items = [MagicMock(spec=WarehouseStockItemModel), MagicMock(spec=WarehouseStockItemModel)]
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.all.return_value = mock_stock_items

        # Act
        result = WarehouseStockItemDAO.get_all()

        # Assert
        mock_session.query.assert_called_once_with(WarehouseStockItemModel)
        mock_query.all.assert_called_once()
        mock_session.close.assert_called_once()
        assert result == mock_stock_items

    @patch('src.infrastructure.dao.warehouse_stock_item_dao.Session')
    def test_get_by_warehouse_id(self, mock_session_class):
        """Test get_by_warehouse_id method"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        warehouse_id = "w123"
        mock_stock_items = [MagicMock(spec=WarehouseStockItemModel), MagicMock(spec=WarehouseStockItemModel)]
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.all.return_value = mock_stock_items

        # Act
        result = WarehouseStockItemDAO.get_by_warehouse_id(warehouse_id)

        # Assert
        mock_session.query.assert_called_once_with(WarehouseStockItemModel)
        mock_query.filter.assert_called_once()
        mock_filter.all.assert_called_once()
        mock_session.close.assert_called_once()
        assert result == mock_stock_items

    @patch('src.infrastructure.dao.warehouse_stock_item_dao.Session')
    def test_get_by_item_id(self, mock_session_class):
        """Test get_by_item_id method"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        item_id = "item123"
        mock_stock_items = [MagicMock(spec=WarehouseStockItemModel), MagicMock(spec=WarehouseStockItemModel)]
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.all.return_value = mock_stock_items

        # Act
        result = WarehouseStockItemDAO.get_by_item_id(item_id)

        # Assert
        mock_session.query.assert_called_once_with(WarehouseStockItemModel)
        mock_query.filter.assert_called_once()
        mock_filter.all.assert_called_once()
        mock_session.close.assert_called_once()
        assert result == mock_stock_items

    @patch('src.infrastructure.dao.warehouse_stock_item_dao.Session')
    def test_get_by_barcode_found(self, mock_session_class):
        """Test get_by_barcode method when stock item exists"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        barcode = "12345678"
        mock_stock_item = MagicMock(spec=WarehouseStockItemModel)
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_stock_item

        # Act
        result = WarehouseStockItemDAO.get_by_barcode(barcode)

        # Assert
        mock_session.query.assert_called_once_with(WarehouseStockItemModel)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        mock_session.close.assert_called_once()
        assert result == mock_stock_item

    @patch('src.infrastructure.dao.warehouse_stock_item_dao.Session')
    def test_get_by_barcode_not_found(self, mock_session_class):
        """Test get_by_barcode method when stock item does not exist"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        barcode = "nonexistent"
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None

        # Act
        result = WarehouseStockItemDAO.get_by_barcode(barcode)

        # Assert
        mock_session.query.assert_called_once_with(WarehouseStockItemModel)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        mock_session.close.assert_called_once()
        assert result is None

    @patch('src.infrastructure.dao.warehouse_stock_item_dao.Session')
    def test_get_by_identification_code_found(self, mock_session_class):
        """Test get_by_identification_code method when stock item exists"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        identification_code = "ID12345"
        mock_stock_item = MagicMock(spec=WarehouseStockItemModel)
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_stock_item

        # Act
        result = WarehouseStockItemDAO.get_by_identification_code(identification_code)

        # Assert
        mock_session.query.assert_called_once_with(WarehouseStockItemModel)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        mock_session.close.assert_called_once()
        assert result == mock_stock_item

    @patch('src.infrastructure.dao.warehouse_stock_item_dao.Session')
    def test_get_by_identification_code_not_found(self, mock_session_class):
        """Test get_by_identification_code method when stock item does not exist"""
        # Arrange
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        identification_code = "nonexistent"
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None

        # Act
        result = WarehouseStockItemDAO.get_by_identification_code(identification_code)

        # Assert
        mock_session.query.assert_called_once_with(WarehouseStockItemModel)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        mock_session.close.assert_called_once()
        assert result is None