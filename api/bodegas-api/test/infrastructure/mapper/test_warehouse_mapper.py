import pytest
from datetime import datetime
from unittest.mock import MagicMock

from src.domain.entities.warehouse_dto import WarehouseDTO
from src.infrastructure.mapper.warehouse_mapper import WarehouseMapper
from src.infrastructure.model.warehouse_model import WarehouseModel


class TestWarehouseMapper:
    """Test suite for WarehouseMapper"""

    def test_to_dto(self):
        """Test conversion from model to DTO"""
        # Arrange
        model = MagicMock(spec=WarehouseModel)
        model.id = "w123"
        model.location = "Test Location"
        model.description = "Test Description"
        model.name = "Test Warehouse"
        model.administrator_id = "admin123"
        model.status = "active"
        model.created_at = datetime(2023, 1, 1, 0, 0, 0)
        model.updated_at = datetime(2023, 1, 2, 0, 0, 0)

        # Act
        result = WarehouseMapper.to_dto(model)

        # Assert
        assert isinstance(result, WarehouseDTO)
        assert result.warehouse_id == "w123"
        assert result.location == "Test Location"
        assert result.description == "Test Description"
        assert result.name == "Test Warehouse"
        assert result.administrator_id == "admin123"
        assert result.status == "active"
        assert result.created_at == "2023-01-01T00:00:00"
        assert result.updated_at == "2023-01-02T00:00:00"

    def test_to_dto_with_none_dates(self):
        """Test conversion from model to DTO with None dates"""
        # Arrange
        model = MagicMock(spec=WarehouseModel)
        model.id = "w123"
        model.location = "Test Location"
        model.description = "Test Description"
        model.name = "Test Warehouse"
        model.administrator_id = "admin123"
        model.status = "active"
        model.created_at = None
        model.updated_at = None

        # Act
        result = WarehouseMapper.to_dto(model)

        # Assert
        assert isinstance(result, WarehouseDTO)
        assert result.warehouse_id == "w123"
        assert result.created_at is None
        assert result.updated_at is None

    def test_to_model(self):
        """Test conversion from DTO to model"""
        # Arrange
        dto = WarehouseDTO(
            warehouse_id="w123",
            location="Test Location",
            description="Test Description",
            name="Test Warehouse",
            administrator_id="admin123",
            status="active",
            created_at="2023-01-01T00:00:00",
            updated_at="2023-01-02T00:00:00"
        )

        # Act
        result = WarehouseMapper.to_model(dto)

        # Assert
        assert isinstance(result, WarehouseModel)
        assert result.id == "w123"
        assert result.location == "Test Location"
        assert result.description == "Test Description"
        assert result.name == "Test Warehouse"
        assert result.administrator_id == "admin123"
        assert result.status == "active"
        # Note: created_at and updated_at are not set in the to_model method

    def test_to_dto_list(self):
        """Test conversion from model list to DTO list"""
        # Arrange
        model1 = MagicMock(spec=WarehouseModel)
        model1.id = "w123"
        model1.location = "Test Location 1"
        model1.description = "Test Description 1"
        model1.name = "Test Warehouse 1"
        model1.administrator_id = "admin123"
        model1.status = "active"
        model1.created_at = datetime(2023, 1, 1, 0, 0, 0)
        model1.updated_at = datetime(2023, 1, 2, 0, 0, 0)

        model2 = MagicMock(spec=WarehouseModel)
        model2.id = "w456"
        model2.location = "Test Location 2"
        model2.description = "Test Description 2"
        model2.name = "Test Warehouse 2"
        model2.administrator_id = "admin456"
        model2.status = "inactive"
        model2.created_at = datetime(2023, 1, 3, 0, 0, 0)
        model2.updated_at = datetime(2023, 1, 4, 0, 0, 0)

        models = [model1, model2]

        # Act
        result = WarehouseMapper.to_dto_list(models)

        # Assert
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, WarehouseDTO) for item in result)
        assert result[0].warehouse_id == "w123"
        assert result[1].warehouse_id == "w456"

    def test_to_model_list(self):
        """Test conversion from DTO list to model list"""
        # Arrange
        dto1 = WarehouseDTO(
            warehouse_id="w123",
            location="Test Location 1",
            description="Test Description 1",
            name="Test Warehouse 1",
            administrator_id="admin123",
            status="active",
            created_at="2023-01-01T00:00:00",
            updated_at="2023-01-02T00:00:00"
        )

        dto2 = WarehouseDTO(
            warehouse_id="w456",
            location="Test Location 2",
            description="Test Description 2",
            name="Test Warehouse 2",
            administrator_id="admin456",
            status="inactive",
            created_at="2023-01-03T00:00:00",
            updated_at="2023-01-04T00:00:00"
        )

        dtos = [dto1, dto2]

        # Act
        result = WarehouseMapper.to_model_list(dtos)

        # Assert
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, WarehouseModel) for item in result)
        assert result[0].id == "w123"
        assert result[1].id == "w456"