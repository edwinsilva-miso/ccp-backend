import pytest
import uuid
from unittest.mock import MagicMock, patch

from src.domain.entities.warehouse_dto import WarehouseDTO
from src.infrastructure.adapters.warehouse_adapter import WarehouseAdapter


class TestWarehouseAdapter:
    """Test suite for WarehouseAdapter"""

    def test_get_by_id_found(self, warehouse_adapter, mock_warehouse_dao, mock_warehouse_mapper, warehouse_dto):
        """Test get_by_id when warehouse is found"""
        # Arrange
        warehouse_id = "w123"
        mock_warehouse = MagicMock()

        # Patch the DAO method to handle the UUID conversion
        with patch('src.infrastructure.adapters.warehouse_adapter.WarehouseDAO.get_by_id') as patched_get_by_id, \
             patch('src.infrastructure.adapters.warehouse_adapter.WarehouseMapper.to_dto') as patched_to_dto:
            patched_get_by_id.return_value = mock_warehouse
            patched_to_dto.return_value = warehouse_dto

            # Act
            result = warehouse_adapter.get_by_id(warehouse_id)

            # Assert
            patched_get_by_id.assert_called_once_with(warehouse_id)
            patched_to_dto.assert_called_once_with(mock_warehouse)
            assert result == warehouse_dto

    def test_get_by_id_not_found(self, warehouse_adapter, mock_warehouse_dao, mock_warehouse_mapper):
        """Test get_by_id when warehouse is not found"""
        # Arrange
        warehouse_id = "nonexistent"

        # Patch the DAO method to handle the UUID conversion
        with patch('src.infrastructure.adapters.warehouse_adapter.WarehouseDAO.get_by_id') as patched_get_by_id, \
             patch('src.infrastructure.adapters.warehouse_adapter.WarehouseMapper.to_dto') as patched_to_dto:
            patched_get_by_id.return_value = None

            # Act
            result = warehouse_adapter.get_by_id(warehouse_id)

            # Assert
            patched_get_by_id.assert_called_once_with(warehouse_id)
            patched_to_dto.assert_not_called()
            assert result is None

    def test_get_all(self, warehouse_adapter, mock_warehouse_dao, mock_warehouse_mapper, warehouse_dto_list):
        """Test get_all warehouses"""
        # Arrange
        mock_warehouses = [MagicMock(), MagicMock()]

        # Patch the DAO method to handle the UUID conversion
        with patch('src.infrastructure.adapters.warehouse_adapter.WarehouseDAO.get_all') as patched_get_all, \
             patch('src.infrastructure.adapters.warehouse_adapter.WarehouseMapper.to_dto_list') as patched_to_dto_list:
            patched_get_all.return_value = mock_warehouses
            patched_to_dto_list.return_value = warehouse_dto_list

            # Act
            result = warehouse_adapter.get_all()

            # Assert
            patched_get_all.assert_called_once()
            patched_to_dto_list.assert_called_once_with(mock_warehouses)
            assert result == warehouse_dto_list

    def test_get_by_administrator_id(self, warehouse_adapter, mock_warehouse_dao, mock_warehouse_mapper, warehouse_dto_list):
        """Test get_by_administrator_id"""
        # Arrange
        admin_id = "admin123"
        mock_warehouses = [MagicMock(), MagicMock()]

        # Patch the DAO method to handle the UUID conversion
        with patch('src.infrastructure.adapters.warehouse_adapter.WarehouseDAO.get_by_administrator_id') as patched_get_by_admin_id, \
             patch('src.infrastructure.adapters.warehouse_adapter.WarehouseMapper.to_dto_list') as patched_to_dto_list:
            patched_get_by_admin_id.return_value = mock_warehouses
            patched_to_dto_list.return_value = warehouse_dto_list

            # Act
            result = warehouse_adapter.get_by_administrator_id(admin_id)

            # Assert
            patched_get_by_admin_id.assert_called_once_with(admin_id)
            patched_to_dto_list.assert_called_once_with(mock_warehouses)
            assert result == warehouse_dto_list

    def test_add(self, warehouse_adapter, mock_warehouse_dao, mock_warehouse_mapper, warehouse_dto):
        """Test add warehouse"""
        # Arrange
        mock_warehouse = MagicMock()
        mock_warehouse_dao_result = MagicMock()

        # Patch the mapper and DAO methods to handle the UUID conversion
        with patch('src.infrastructure.adapters.warehouse_adapter.WarehouseMapper.to_model') as patched_to_model, \
             patch('src.infrastructure.adapters.warehouse_adapter.WarehouseDAO.save') as patched_save, \
             patch('src.infrastructure.adapters.warehouse_adapter.WarehouseMapper.to_dto') as patched_to_dto:

            patched_to_model.return_value = mock_warehouse
            patched_save.return_value = mock_warehouse_dao_result
            patched_to_dto.return_value = warehouse_dto

            # Act
            result = warehouse_adapter.add(warehouse_dto)

            # Assert
            patched_to_model.assert_called_once_with(warehouse_dto)
            patched_save.assert_called_once_with(mock_warehouse)
            patched_to_dto.assert_called_once_with(mock_warehouse_dao_result)
            assert result == warehouse_dto

    def test_update(self, warehouse_adapter, mock_warehouse_dao, mock_warehouse_mapper, warehouse_dto):
        """Test update warehouse"""
        # Arrange
        mock_warehouse = MagicMock()
        mock_warehouse_dao_result = MagicMock()

        # Patch the mapper and DAO methods to handle the UUID conversion
        with patch('src.infrastructure.adapters.warehouse_adapter.WarehouseMapper.to_model') as patched_to_model, \
             patch('src.infrastructure.adapters.warehouse_adapter.WarehouseDAO.update') as patched_update, \
             patch('src.infrastructure.adapters.warehouse_adapter.WarehouseMapper.to_dto') as patched_to_dto:

            patched_to_model.return_value = mock_warehouse
            patched_update.return_value = mock_warehouse_dao_result
            patched_to_dto.return_value = warehouse_dto

            # Act
            result = warehouse_adapter.update(warehouse_dto)

            # Assert
            patched_to_model.assert_called_once_with(warehouse_dto)
            patched_update.assert_called_once_with(mock_warehouse)
            patched_to_dto.assert_called_once_with(mock_warehouse_dao_result)
            assert result == warehouse_dto

    def test_delete(self, warehouse_adapter, mock_warehouse_dao):
        """Test delete warehouse"""
        # Arrange
        warehouse_id = "w123"

        # Patch the DAO method to handle the UUID conversion
        with patch('src.infrastructure.adapters.warehouse_adapter.WarehouseDAO.delete') as patched_delete:
            patched_delete.return_value = True

            # Act
            result = warehouse_adapter.delete(warehouse_id)

            # Assert
            patched_delete.assert_called_once_with(warehouse_id)
            assert result is True

    def test_delete_failure(self, warehouse_adapter, mock_warehouse_dao):
        """Test delete warehouse failure"""
        # Arrange
        warehouse_id = "nonexistent"

        # Patch the DAO method to handle the UUID conversion
        with patch('src.infrastructure.adapters.warehouse_adapter.WarehouseDAO.delete') as patched_delete:
            patched_delete.return_value = False

            # Act
            result = warehouse_adapter.delete(warehouse_id)

            # Assert
            patched_delete.assert_called_once_with(warehouse_id)
            assert result is False
