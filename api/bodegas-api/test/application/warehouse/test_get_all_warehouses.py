import pytest
from unittest.mock import MagicMock

from src.application.warehouse.get_all_warehouses import GetAllWarehouses
from src.domain.entities.warehouse_dto import WarehouseDTO
from src.domain.repositories.warehouse_repository import WarehouseRepository


class TestGetAllWarehouses:
    """Test suite for GetAllWarehouses use case"""

    def test_execute_with_warehouses(self):
        """Test execution of GetAllWarehouses use case when warehouses exist"""
        # Arrange
        warehouses = [
            WarehouseDTO(
                warehouse_id="w123",
                location="Test Location 1",
                description="Test Description 1",
                name="Test Warehouse 1",
                administrator_id="admin123",
                status="active",
                created_at="2023-01-01T00:00:00",
                updated_at="2023-01-01T00:00:00"
            ),
            WarehouseDTO(
                warehouse_id="w456",
                location="Test Location 2",
                description="Test Description 2",
                name="Test Warehouse 2",
                administrator_id="admin456",
                status="inactive",
                created_at="2023-01-02T00:00:00",
                updated_at="2023-01-02T00:00:00"
            )
        ]
        
        # Mock the repository
        mock_repository = MagicMock(spec=WarehouseRepository)
        mock_repository.get_all.return_value = warehouses
        
        # Create the use case with the mocked repository
        use_case = GetAllWarehouses(mock_repository)
        
        # Act
        result = use_case.execute()
        
        # Assert
        mock_repository.get_all.assert_called_once()
        assert result == warehouses
        assert len(result) == 2
        assert result[0].warehouse_id == "w123"
        assert result[1].warehouse_id == "w456"

    def test_execute_with_empty_list(self):
        """Test execution of GetAllWarehouses use case when no warehouses exist"""
        # Arrange
        warehouses = []
        
        # Mock the repository
        mock_repository = MagicMock(spec=WarehouseRepository)
        mock_repository.get_all.return_value = warehouses
        
        # Create the use case with the mocked repository
        use_case = GetAllWarehouses(mock_repository)
        
        # Act
        result = use_case.execute()
        
        # Assert
        mock_repository.get_all.assert_called_once()
        assert result == warehouses
        assert len(result) == 0