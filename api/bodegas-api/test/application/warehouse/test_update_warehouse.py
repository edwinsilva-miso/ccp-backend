import pytest
from unittest.mock import MagicMock

from src.application.warehouse.update_warehouse import UpdateWarehouse
from src.application.errors.errors import ResourceNotFoundError
from src.domain.entities.warehouse_dto import WarehouseDTO
from src.domain.repositories.warehouse_repository import WarehouseRepository


class TestUpdateWarehouse:
    """Test suite for UpdateWarehouse use case"""

    def test_execute_success(self):
        """Test successful execution of UpdateWarehouse use case"""
        # Arrange
        warehouse_dto = WarehouseDTO(
            warehouse_id="w123",
            location="Updated Location",
            description="Updated Description",
            name="Updated Warehouse",
            administrator_id="admin123",
            status="active"
        )
        
        expected_result = WarehouseDTO(
            warehouse_id="w123",
            location="Updated Location",
            description="Updated Description",
            name="Updated Warehouse",
            administrator_id="admin123",
            status="active",
            created_at="2023-01-01T00:00:00",
            updated_at="2023-01-02T00:00:00"
        )
        
        # Mock the repository
        mock_repository = MagicMock(spec=WarehouseRepository)
        mock_repository.get_by_id.return_value = warehouse_dto  # Warehouse exists
        mock_repository.update.return_value = expected_result
        
        # Create the use case with the mocked repository
        use_case = UpdateWarehouse(mock_repository)
        
        # Act
        result = use_case.execute(warehouse_dto)
        
        # Assert
        mock_repository.get_by_id.assert_called_once_with(warehouse_dto.warehouse_id)
        mock_repository.update.assert_called_once_with(warehouse_dto)
        assert result == expected_result
        assert result.warehouse_id == "w123"
        assert result.name == "Updated Warehouse"
        assert result.location == "Updated Location"
        assert result.description == "Updated Description"
        assert result.administrator_id == "admin123"
        assert result.status == "active"
        assert result.updated_at == "2023-01-02T00:00:00"

    def test_execute_warehouse_not_found(self):
        """Test execution of UpdateWarehouse use case when warehouse is not found"""
        # Arrange
        warehouse_dto = WarehouseDTO(
            warehouse_id="nonexistent",
            location="Updated Location",
            description="Updated Description",
            name="Updated Warehouse",
            administrator_id="admin123",
            status="active"
        )
        
        # Mock the repository
        mock_repository = MagicMock(spec=WarehouseRepository)
        mock_repository.get_by_id.return_value = None  # Warehouse doesn't exist
        
        # Create the use case with the mocked repository
        use_case = UpdateWarehouse(mock_repository)
        
        # Act & Assert
        with pytest.raises(ResourceNotFoundError):
            use_case.execute(warehouse_dto)
        
        mock_repository.get_by_id.assert_called_once_with(warehouse_dto.warehouse_id)
        mock_repository.update.assert_not_called()