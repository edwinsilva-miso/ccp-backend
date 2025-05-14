import pytest
import uuid
from unittest.mock import MagicMock, patch

from src.domain.entities.warehouse_stock_item_dto import WarehouseStockItemDTO
from src.infrastructure.adapters.warehouse_stock_item_adapter import WarehouseStockItemAdapter


class TestWarehouseStockItemAdapter:
    """Test suite for WarehouseStockItemAdapter"""

    def test_get_by_id_found(self, warehouse_stock_item_adapter, mock_warehouse_stock_item_dao, 
                            mock_warehouse_stock_item_mapper, warehouse_stock_item_dto):
        """Test get_by_id when stock item is found"""
        # Arrange
        item_id = "wsi123"
        mock_stock_item = MagicMock()

        # Patch the DAO method to handle the UUID conversion
        with patch('src.infrastructure.adapters.warehouse_stock_item_adapter.WarehouseStockItemDAO.get_by_id') as patched_get_by_id:
            patched_get_by_id.return_value = mock_stock_item
            mock_warehouse_stock_item_mapper.to_dto.return_value = warehouse_stock_item_dto

            # Act
            result = warehouse_stock_item_adapter.get_by_id(item_id)

            # Assert
            patched_get_by_id.assert_called_once_with(item_id)
            mock_warehouse_stock_item_mapper.to_dto.assert_called_once_with(mock_stock_item)
            assert result == warehouse_stock_item_dto

    def test_get_by_id_not_found(self, warehouse_stock_item_adapter, mock_warehouse_stock_item_dao, 
                                mock_warehouse_stock_item_mapper):
        """Test get_by_id when stock item is not found"""
        # Arrange
        item_id = "nonexistent"

        # Patch the DAO method to handle the UUID conversion
        with patch('src.infrastructure.adapters.warehouse_stock_item_adapter.WarehouseStockItemDAO.get_by_id') as patched_get_by_id:
            patched_get_by_id.return_value = None

            # Act
            result = warehouse_stock_item_adapter.get_by_id(item_id)

            # Assert
            patched_get_by_id.assert_called_once_with(item_id)
            mock_warehouse_stock_item_mapper.to_dto.assert_not_called()
            assert result is None

    def test_get_all(self, warehouse_stock_item_adapter, mock_warehouse_stock_item_dao, 
                    mock_warehouse_stock_item_mapper, warehouse_stock_item_dto_list):
        """Test get_all stock items"""
        # Arrange
        mock_stock_items = [MagicMock(), MagicMock()]

        # Patch the DAO method to handle the UUID conversion
        with patch('src.infrastructure.adapters.warehouse_stock_item_adapter.WarehouseStockItemDAO.get_all') as patched_get_all:
            patched_get_all.return_value = mock_stock_items
            mock_warehouse_stock_item_mapper.to_dto_list.return_value = warehouse_stock_item_dto_list

            # Act
            result = warehouse_stock_item_adapter.get_all()

            # Assert
            patched_get_all.assert_called_once()
            mock_warehouse_stock_item_mapper.to_dto_list.assert_called_once_with(mock_stock_items)
            assert result == warehouse_stock_item_dto_list

    def test_get_by_warehouse_id(self, warehouse_stock_item_adapter, mock_warehouse_stock_item_dao, 
                                mock_warehouse_stock_item_mapper, warehouse_stock_item_dto_list):
        """Test get_by_warehouse_id"""
        # Arrange
        warehouse_id = "w123"
        mock_stock_items = [MagicMock(), MagicMock()]
        mock_warehouse_stock_item_dao.get_by_warehouse_id.return_value = mock_stock_items
        mock_warehouse_stock_item_mapper.to_dto_list.return_value = warehouse_stock_item_dto_list

        # Act
        result = warehouse_stock_item_adapter.get_by_warehouse_id(warehouse_id)

        # Assert
        mock_warehouse_stock_item_dao.get_by_warehouse_id.assert_called_once_with(warehouse_id)
        mock_warehouse_stock_item_mapper.to_dto_list.assert_called_once_with(mock_stock_items)
        assert result == warehouse_stock_item_dto_list

    def test_get_by_item_id(self, warehouse_stock_item_adapter, mock_warehouse_stock_item_dao, 
                            mock_warehouse_stock_item_mapper, warehouse_stock_item_dto_list):
        """Test get_by_item_id"""
        # Arrange
        item_id = "item123"
        mock_stock_items = [MagicMock(), MagicMock()]
        mock_warehouse_stock_item_dao.get_by_item_id.return_value = mock_stock_items
        mock_warehouse_stock_item_mapper.to_dto_list.return_value = warehouse_stock_item_dto_list

        # Act
        result = warehouse_stock_item_adapter.get_by_item_id(item_id)

        # Assert
        mock_warehouse_stock_item_dao.get_by_item_id.assert_called_once_with(item_id)
        mock_warehouse_stock_item_mapper.to_dto_list.assert_called_once_with(mock_stock_items)
        assert result == warehouse_stock_item_dto_list

    def test_get_by_barcode_found(self, warehouse_stock_item_adapter, mock_warehouse_stock_item_dao, 
                                mock_warehouse_stock_item_mapper, warehouse_stock_item_dto):
        """Test get_by_barcode when stock item is found"""
        # Arrange
        barcode = "12345678"
        mock_stock_item = MagicMock()
        mock_warehouse_stock_item_dao.get_by_barcode.return_value = mock_stock_item
        mock_warehouse_stock_item_mapper.to_dto.return_value = warehouse_stock_item_dto

        # Act
        result = warehouse_stock_item_adapter.get_by_barcode(barcode)

        # Assert
        mock_warehouse_stock_item_dao.get_by_barcode.assert_called_once_with(barcode)
        mock_warehouse_stock_item_mapper.to_dto.assert_called_once_with(mock_stock_item)
        assert result == warehouse_stock_item_dto

    def test_get_by_barcode_not_found(self, warehouse_stock_item_adapter, mock_warehouse_stock_item_dao, 
                                    mock_warehouse_stock_item_mapper):
        """Test get_by_barcode when stock item is not found"""
        # Arrange
        barcode = "nonexistent"
        mock_warehouse_stock_item_dao.get_by_barcode.return_value = None

        # Act
        result = warehouse_stock_item_adapter.get_by_barcode(barcode)

        # Assert
        mock_warehouse_stock_item_dao.get_by_barcode.assert_called_once_with(barcode)
        mock_warehouse_stock_item_mapper.to_dto.assert_not_called()
        assert result is None

    def test_get_by_identification_code_found(self, warehouse_stock_item_adapter, mock_warehouse_stock_item_dao, 
                                            mock_warehouse_stock_item_mapper, warehouse_stock_item_dto):
        """Test get_by_identification_code when stock item is found"""
        # Arrange
        identification_code = "ID12345"
        mock_stock_item = MagicMock()
        mock_warehouse_stock_item_dao.get_by_identification_code.return_value = mock_stock_item
        mock_warehouse_stock_item_mapper.to_dto.return_value = warehouse_stock_item_dto

        # Act
        result = warehouse_stock_item_adapter.get_by_identification_code(identification_code)

        # Assert
        mock_warehouse_stock_item_dao.get_by_identification_code.assert_called_once_with(identification_code)
        mock_warehouse_stock_item_mapper.to_dto.assert_called_once_with(mock_stock_item)
        assert result == warehouse_stock_item_dto

    def test_get_by_identification_code_not_found(self, warehouse_stock_item_adapter, mock_warehouse_stock_item_dao, 
                                                mock_warehouse_stock_item_mapper):
        """Test get_by_identification_code when stock item is not found"""
        # Arrange
        identification_code = "nonexistent"
        mock_warehouse_stock_item_dao.get_by_identification_code.return_value = None

        # Act
        result = warehouse_stock_item_adapter.get_by_identification_code(identification_code)

        # Assert
        mock_warehouse_stock_item_dao.get_by_identification_code.assert_called_once_with(identification_code)
        mock_warehouse_stock_item_mapper.to_dto.assert_not_called()
        assert result is None

    def test_add(self, warehouse_stock_item_adapter, mock_warehouse_stock_item_dao, 
                mock_warehouse_stock_item_mapper, warehouse_stock_item_dto):
        """Test add stock item"""
        # Arrange
        mock_stock_item = MagicMock()
        mock_stock_item_dao_result = MagicMock()
        mock_warehouse_stock_item_mapper.to_model.return_value = mock_stock_item
        mock_warehouse_stock_item_dao.save.return_value = mock_stock_item_dao_result
        mock_warehouse_stock_item_mapper.to_dto.return_value = warehouse_stock_item_dto

        # Act
        result = warehouse_stock_item_adapter.add(warehouse_stock_item_dto)

        # Assert
        mock_warehouse_stock_item_mapper.to_model.assert_called_once_with(warehouse_stock_item_dto)
        mock_warehouse_stock_item_dao.save.assert_called_once_with(mock_stock_item)
        mock_warehouse_stock_item_mapper.to_dto.assert_called_once_with(mock_stock_item_dao_result)
        assert result == warehouse_stock_item_dto

    def test_update(self, warehouse_stock_item_adapter, mock_warehouse_stock_item_dao, 
                    mock_warehouse_stock_item_mapper, warehouse_stock_item_dto):
        """Test update stock item"""
        # Arrange
        mock_stock_item = MagicMock()
        mock_stock_item_dao_result = MagicMock()
        mock_warehouse_stock_item_mapper.to_model.return_value = mock_stock_item
        mock_warehouse_stock_item_dao.update.return_value = mock_stock_item_dao_result
        mock_warehouse_stock_item_mapper.to_dto.return_value = warehouse_stock_item_dto

        # Act
        result = warehouse_stock_item_adapter.update(warehouse_stock_item_dto)

        # Assert
        mock_warehouse_stock_item_mapper.to_model.assert_called_once_with(warehouse_stock_item_dto)
        mock_warehouse_stock_item_dao.update.assert_called_once_with(mock_stock_item)
        mock_warehouse_stock_item_mapper.to_dto.assert_called_once_with(mock_stock_item_dao_result)
        assert result == warehouse_stock_item_dto

    def test_delete(self, warehouse_stock_item_adapter, mock_warehouse_stock_item_dao):
        """Test delete stock item"""
        # Arrange
        item_id = "wsi123"
        mock_warehouse_stock_item_dao.delete.return_value = True

        # Act
        result = warehouse_stock_item_adapter.delete(item_id)

        # Assert
        mock_warehouse_stock_item_dao.delete.assert_called_once_with(item_id)
        assert result is True

    def test_delete_failure(self, warehouse_stock_item_adapter, mock_warehouse_stock_item_dao):
        """Test delete stock item failure"""
        # Arrange
        item_id = "nonexistent"
        mock_warehouse_stock_item_dao.delete.return_value = False

        # Act
        result = warehouse_stock_item_adapter.delete(item_id)

        # Assert
        mock_warehouse_stock_item_dao.delete.assert_called_once_with(item_id)
        assert result is False
