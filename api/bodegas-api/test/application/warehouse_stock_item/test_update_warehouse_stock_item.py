import pytest
from unittest.mock import MagicMock

from src.application.warehouse_stock_item.update_warehouse_stock_item import UpdateWarehouseStockItem
from src.application.errors.errors import ResourceNotFoundError
from src.domain.entities.warehouse_stock_item_dto import WarehouseStockItemDTO
from src.domain.repositories.warehouse_stock_item_repository import WarehouseStockItemRepository


class TestUpdateWarehouseStockItem:
    """Test suite for UpdateWarehouseStockItem use case"""

    def test_execute_success(self):
        """Test successful execution of UpdateWarehouseStockItem use case"""
        # Arrange
        warehouse_stock_item_dto = WarehouseStockItemDTO(
            warehouse_stock_item_id="wsi123",
            warehouse_id="w123",
            item_id="item123",
            bar_code="87654321",  # Updated value
            identification_code="ID54321",  # Updated value
            width=15.0,  # Updated value
            height=25.0,  # Updated value
            depth=35.0,  # Updated value
            weight=7.5,  # Updated value
            hallway="B",  # Updated value
            shelf="2",  # Updated value
            sold=True,  # Updated value
            status="active"
        )
        
        expected_result = WarehouseStockItemDTO(
            warehouse_stock_item_id="wsi123",
            warehouse_id="w123",
            item_id="item123",
            bar_code="87654321",
            identification_code="ID54321",
            width=15.0,
            height=25.0,
            depth=35.0,
            weight=7.5,
            hallway="B",
            shelf="2",
            sold=True,
            status="active",
            created_at="2023-01-01T00:00:00",
            updated_at="2023-01-02T00:00:00"  # Updated timestamp
        )
        
        # Mock the repository
        mock_repository = MagicMock(spec=WarehouseStockItemRepository)
        mock_repository.get_by_id.return_value = warehouse_stock_item_dto  # Item exists
        mock_repository.update.return_value = expected_result
        
        # Create the use case with the mocked repository
        use_case = UpdateWarehouseStockItem(mock_repository)
        
        # Act
        result = use_case.execute(warehouse_stock_item_dto)
        
        # Assert
        mock_repository.get_by_id.assert_called_once_with(warehouse_stock_item_dto.warehouse_stock_item_id)
        mock_repository.update.assert_called_once_with(warehouse_stock_item_dto)
        assert result == expected_result
        assert result.warehouse_stock_item_id == "wsi123"
        assert result.warehouse_id == "w123"
        assert result.item_id == "item123"
        assert result.bar_code == "87654321"
        assert result.identification_code == "ID54321"
        assert result.width == 15.0
        assert result.height == 25.0
        assert result.depth == 35.0
        assert result.weight == 7.5
        assert result.hallway == "B"
        assert result.shelf == "2"
        assert result.sold is True
        assert result.status == "active"
        assert result.updated_at == "2023-01-02T00:00:00"

    def test_execute_item_not_found(self):
        """Test execution of UpdateWarehouseStockItem use case when item is not found"""
        # Arrange
        warehouse_stock_item_dto = WarehouseStockItemDTO(
            warehouse_stock_item_id="nonexistent",
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
        
        # Mock the repository
        mock_repository = MagicMock(spec=WarehouseStockItemRepository)
        mock_repository.get_by_id.return_value = None  # Item doesn't exist
        
        # Create the use case with the mocked repository
        use_case = UpdateWarehouseStockItem(mock_repository)
        
        # Act & Assert
        with pytest.raises(ResourceNotFoundError):
            use_case.execute(warehouse_stock_item_dto)
        
        mock_repository.get_by_id.assert_called_once_with(warehouse_stock_item_dto.warehouse_stock_item_id)
        mock_repository.update.assert_not_called()