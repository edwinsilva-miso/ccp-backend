import pytest
from datetime import datetime
from unittest.mock import MagicMock

from src.domain.entities.warehouse_stock_item_dto import WarehouseStockItemDTO
from src.infrastructure.mapper.warehouse_stock_item_mapper import WarehouseStockItemMapper
from src.infrastructure.model.warehouse_stock_item_model import WarehouseStockItemModel


class TestWarehouseStockItemMapper:
    """Test suite for WarehouseStockItemMapper"""

    def test_to_dto(self):
        """Test conversion from model to DTO"""
        # Arrange
        model = MagicMock(spec=WarehouseStockItemModel)
        model.warehouse_stock_item_id = "wsi123"
        model.warehouse_id = "w123"
        model.item_id = "item123"
        model.bar_code = "12345678"
        model.identification_code = "ID12345"
        model.width = 10.0
        model.height = 20.0
        model.depth = 30.0
        model.weight = 5.0
        model.hallway = "A"
        model.shelf = "1"
        model.sold = False
        model.status = "active"
        model.created_at = datetime(2023, 1, 1, 0, 0, 0)
        model.updated_at = datetime(2023, 1, 2, 0, 0, 0)

        # Act
        result = WarehouseStockItemMapper.to_dto(model)

        # Assert
        assert isinstance(result, WarehouseStockItemDTO)
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
        assert result.created_at == "2023-01-01T00:00:00"
        assert result.updated_at == "2023-01-02T00:00:00"

    def test_to_dto_with_none_dates(self):
        """Test conversion from model to DTO with None dates"""
        # Arrange
        model = MagicMock(spec=WarehouseStockItemModel)
        model.warehouse_stock_item_id = "wsi123"
        model.warehouse_id = "w123"
        model.item_id = "item123"
        model.bar_code = "12345678"
        model.identification_code = "ID12345"
        model.width = 10.0
        model.height = 20.0
        model.depth = 30.0
        model.weight = 5.0
        model.hallway = "A"
        model.shelf = "1"
        model.sold = False
        model.status = "active"
        model.created_at = None
        model.updated_at = None

        # Act
        result = WarehouseStockItemMapper.to_dto(model)

        # Assert
        assert isinstance(result, WarehouseStockItemDTO)
        assert result.warehouse_stock_item_id == "wsi123"
        assert result.created_at is None
        assert result.updated_at is None

    def test_to_model(self):
        """Test conversion from DTO to model"""
        # Arrange
        dto = WarehouseStockItemDTO(
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
            updated_at="2023-01-02T00:00:00"
        )

        # Act
        result = WarehouseStockItemMapper.to_model(dto)

        # Assert
        assert isinstance(result, WarehouseStockItemModel)
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
        # Note: created_at and updated_at are not set in the to_model method

    def test_to_dto_list(self):
        """Test conversion from model list to DTO list"""
        # Arrange
        model1 = MagicMock(spec=WarehouseStockItemModel)
        model1.warehouse_stock_item_id = "wsi123"
        model1.warehouse_id = "w123"
        model1.item_id = "item123"
        model1.bar_code = "12345678"
        model1.identification_code = "ID12345"
        model1.width = 10.0
        model1.height = 20.0
        model1.depth = 30.0
        model1.weight = 5.0
        model1.hallway = "A"
        model1.shelf = "1"
        model1.sold = False
        model1.status = "active"
        model1.created_at = datetime(2023, 1, 1, 0, 0, 0)
        model1.updated_at = datetime(2023, 1, 2, 0, 0, 0)

        model2 = MagicMock(spec=WarehouseStockItemModel)
        model2.warehouse_stock_item_id = "wsi456"
        model2.warehouse_id = "w123"
        model2.item_id = "item456"
        model2.bar_code = "87654321"
        model2.identification_code = "ID54321"
        model2.width = 15.0
        model2.height = 25.0
        model2.depth = 35.0
        model2.weight = 7.5
        model2.hallway = "B"
        model2.shelf = "2"
        model2.sold = True
        model2.status = "inactive"
        model2.created_at = datetime(2023, 1, 3, 0, 0, 0)
        model2.updated_at = datetime(2023, 1, 4, 0, 0, 0)

        models = [model1, model2]

        # Act
        result = WarehouseStockItemMapper.to_dto_list(models)

        # Assert
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, WarehouseStockItemDTO) for item in result)
        assert result[0].warehouse_stock_item_id == "wsi123"
        assert result[1].warehouse_stock_item_id == "wsi456"

    def test_to_model_list(self):
        """Test conversion from DTO list to model list"""
        # Arrange
        dto1 = WarehouseStockItemDTO(
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
            updated_at="2023-01-02T00:00:00"
        )

        dto2 = WarehouseStockItemDTO(
            warehouse_stock_item_id="wsi456",
            warehouse_id="w123",
            item_id="item456",
            bar_code="87654321",
            identification_code="ID54321",
            width=15.0,
            height=25.0,
            depth=35.0,
            weight=7.5,
            hallway="B",
            shelf="2",
            sold=True,
            status="inactive",
            created_at="2023-01-03T00:00:00",
            updated_at="2023-01-04T00:00:00"
        )

        dtos = [dto1, dto2]

        # Act
        result = WarehouseStockItemMapper.to_model_list(dtos)

        # Assert
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, WarehouseStockItemModel) for item in result)
        assert result[0].warehouse_stock_item_id == "wsi123"
        assert result[1].warehouse_stock_item_id == "wsi456"