import pytest
from unittest.mock import MagicMock

from src.application.warehouse.get_warehouses_by_administrator_id import GetWarehousesByAdministratorId
from src.domain.entities.warehouse_dto import WarehouseDTO
from src.domain.repositories.warehouse_repository import WarehouseRepository


class TestGetWarehousesByAdministratorId:
    """Test suite for GetWarehousesByAdministratorId use case"""

    def test_execute_with_warehouses(self):
        """Test execution of GetWarehousesByAdministratorId use case when warehouses exist for the administrator"""
        # Arrange
        administrator_id = "admin123"
        warehouses = [
            WarehouseDTO(
                warehouse_id="w123",
                location="Test Location 1",
                description="Test Description 1",
                name="Test Warehouse 1",
                administrator_id=administrator_id,
                status="active",
                created_at="2023-01-01T00:00:00",
                updated_at="2023-01-01T00:00:00"
            ),
            WarehouseDTO(
                warehouse_id="w456",
                location="Test Location 2",
                description="Test Description 2",
                name="Test Warehouse 2",
                administrator_id=administrator_id,
                status="inactive",
                created_at="2023-01-02T00:00:00",
                updated_at="2023-01-02T00:00:00"
            )
        ]
        
        # Mock the repository
        mock_repository = MagicMock(spec=WarehouseRepository)
        mock_repository.get_by_administrator_id.return_value = warehouses
        
        # Create the use case with the mocked repository
        use_case = GetWarehousesByAdministratorId(mock_repository)
        
        # Act
        result = use_case.execute(administrator_id)
        
        # Assert
        mock_repository.get_by_administrator_id.assert_called_once_with(administrator_id)
        assert result == warehouses
        assert len(result) == 2
        assert result[0].warehouse_id == "w123"
        assert result[1].warehouse_id == "w456"
        assert result[0].administrator_id == administrator_id
        assert result[1].administrator_id == administrator_id

    def test_execute_with_empty_list(self):
        """Test execution of GetWarehousesByAdministratorId use case when no warehouses exist for the administrator"""
        # Arrange
        administrator_id = "admin_without_warehouses"
        warehouses = []
        
        # Mock the repository
        mock_repository = MagicMock(spec=WarehouseRepository)
        mock_repository.get_by_administrator_id.return_value = warehouses
        
        # Create the use case with the mocked repository
        use_case = GetWarehousesByAdministratorId(mock_repository)
        
        # Act
        result = use_case.execute(administrator_id)
        
        # Assert
        mock_repository.get_by_administrator_id.assert_called_once_with(administrator_id)
        assert result == warehouses
        assert len(result) == 0