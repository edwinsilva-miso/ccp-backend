import pytest
from unittest.mock import MagicMock

from src.application.warehouse_stock_item.create_warehouse_stock_item import CreateWarehouseStockItem
from src.domain.entities.warehouse_stock_item_dto import WarehouseStockItemDTO
from src.domain.repositories.warehouse_stock_item_repository import WarehouseStockItemRepository


class TestCreateWarehouseStockItem:
    """Test suite for CreateWarehouseStockItem use case"""

    def test_execute_success(self):
        """Test successful execution of CreateWarehouseStockItem use case"""
        # Arrange
        warehouse_stock_item_dto = WarehouseStockItemDTO(
            warehouse_stock_item_id=None,
            warehouse_id="w123",
            item_id="item123",
            bar_code="12345678",
            identification_code="ID12345",
            width=10.0,
            height=20.0,
            depth=30.0,
            weight=5.0,
            hallway="A",
            shelf="1",
            sold=False,
            status="active"
        )
        
        expected_result = WarehouseStockItemDTO(
            warehouse_stock_item_id="wsi123",
            warehouse_id="w123",
            item_id="item123",
            bar_code="12345678",
            identification_code="ID12345",
            width=10.0,
            height=20.0,
            depth=30.0,
            weight=5.0,
            hallway="A",
            shelf="1",
            sold=False,
            status="active",
            created_at="2023-01-01T00:00:00",
            updated_at="2023-01-01T00:00:00"
        )
        
        # Mock the repository
        mock_repository = MagicMock(spec=WarehouseStockItemRepository)
        mock_repository.add.return_value = expected_result
        
        # Create the use case with the mocked repository
        use_case = CreateWarehouseStockItem(mock_repository)
        
        # Act
        result = use_case.execute(warehouse_stock_item_dto)
        
        # Assert
        mock_repository.add.assert_called_once_with(warehouse_stock_item_dto)
        assert result == expected_result
        assert result.warehouse_stock_item_id == "wsi123"
        assert result.warehouse_id == "w123"
        assert result.item_id == "item123"
        assert result.bar_code == "12345678"
        assert result.identification_code == "ID12345"
        assert result.width == 10.0
        assert result.height == 20.0
        assert result.depth == 30.0
        assert result.weight == 5.0
        assert result.hallway == "A"
        assert result.shelf == "1"
        assert result.sold is False
        assert result.status == "active"