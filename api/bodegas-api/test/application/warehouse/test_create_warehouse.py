import pytest
from unittest.mock import MagicMock

from src.application.warehouse.create_warehouse import CreateWarehouse
from src.domain.entities.warehouse_dto import WarehouseDTO
from src.domain.repositories.warehouse_repository import WarehouseRepository


class TestCreateWarehouse:
    """Test suite for CreateWarehouse use case"""

    def test_execute_success(self):
        """Test successful execution of CreateWarehouse use case"""
        # Arrange
        warehouse_dto = WarehouseDTO(
            warehouse_id=None,
            location="Test Location",
            description="Test Description",
            name="Test Warehouse",
            administrator_id="admin123",
            status="active"
        )
        
        expected_result = WarehouseDTO(
            warehouse_id="w123",
            location="Test Location",
            description="Test Description",
            name="Test Warehouse",
            administrator_id="admin123",
            status="active",
            created_at="2023-01-01T00:00:00",
            updated_at="2023-01-01T00:00:00"
        )
        
        # Mock the repository
        mock_repository = MagicMock(spec=WarehouseRepository)
        mock_repository.add.return_value = expected_result
        
        # Create the use case with the mocked repository
        use_case = CreateWarehouse(mock_repository)
        
        # Act
        result = use_case.execute(warehouse_dto)
        
        # Assert
        mock_repository.add.assert_called_once_with(warehouse_dto)
        assert result == expected_result
        assert result.warehouse_id == "w123"
        assert result.name == "Test Warehouse"
        assert result.location == "Test Location"
        assert result.description == "Test Description"
        assert result.administrator_id == "admin123"
        assert result.status == "active"