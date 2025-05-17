import pytest
from unittest.mock import MagicMock

from src.application.warehouse.get_warehouse_by_id import GetWarehouseById
from src.application.errors.errors import ResourceNotFoundError
from src.domain.entities.warehouse_dto import WarehouseDTO
from src.domain.repositories.warehouse_repository import WarehouseRepository


class TestGetWarehouseById:
    """Test suite for GetWarehouseById use case"""

    def test_execute_success(self):
        """Test successful execution of GetWarehouseById use case"""
        # Arrange
        warehouse_id = "w123"
        expected_warehouse = WarehouseDTO(
            warehouse_id=warehouse_id,
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
        mock_repository.get_by_id.return_value = expected_warehouse  # Warehouse exists
        
        # Create the use case with the mocked repository
        use_case = GetWarehouseById(mock_repository)
        
        # Act
        result = use_case.execute(warehouse_id)
        
        # Assert
        mock_repository.get_by_id.assert_called_once_with(warehouse_id)
        assert result == expected_warehouse
        assert result.warehouse_id == warehouse_id
        assert result.name == "Test Warehouse"
        assert result.location == "Test Location"
        assert result.description == "Test Description"
        assert result.administrator_id == "admin123"
        assert result.status == "active"

    def test_execute_warehouse_not_found(self):
        """Test execution of GetWarehouseById use case when warehouse is not found"""
        # Arrange
        warehouse_id = "nonexistent"
        
        # Mock the repository
        mock_repository = MagicMock(spec=WarehouseRepository)
        mock_repository.get_by_id.return_value = None  # Warehouse doesn't exist
        
        # Create the use case with the mocked repository
        use_case = GetWarehouseById(mock_repository)
        
        # Act & Assert
        with pytest.raises(ResourceNotFoundError):
            use_case.execute(warehouse_id)
        
        mock_repository.get_by_id.assert_called_once_with(warehouse_id)