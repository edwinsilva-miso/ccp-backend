import pytest
from unittest.mock import MagicMock

from src.application.warehouse.delete_warehouse import DeleteWarehouse
from src.application.errors.errors import ResourceNotFoundError
from src.domain.entities.warehouse_dto import WarehouseDTO
from src.domain.repositories.warehouse_repository import WarehouseRepository


class TestDeleteWarehouse:
    """Test suite for DeleteWarehouse use case"""

    def test_execute_success(self):
        """Test successful execution of DeleteWarehouse use case"""
        # Arrange
        warehouse_id = "w123"
        existing_warehouse = WarehouseDTO(
            warehouse_id=warehouse_id,
            location="Test Location",
            description="Test Description",
            name="Test Warehouse",
            administrator_id="admin123",
            status="active"
        )
        
        # Mock the repository
        mock_repository = MagicMock(spec=WarehouseRepository)
        mock_repository.get_by_id.return_value = existing_warehouse  # Warehouse exists
        mock_repository.delete.return_value = True  # Deletion successful
        
        # Create the use case with the mocked repository
        use_case = DeleteWarehouse(mock_repository)
        
        # Act
        result = use_case.execute(warehouse_id)
        
        # Assert
        mock_repository.get_by_id.assert_called_once_with(warehouse_id)
        mock_repository.delete.assert_called_once_with(warehouse_id)
        assert result is True

    def test_execute_deletion_failure(self):
        """Test execution of DeleteWarehouse use case when deletion fails"""
        # Arrange
        warehouse_id = "w123"
        existing_warehouse = WarehouseDTO(
            warehouse_id=warehouse_id,
            location="Test Location",
            description="Test Description",
            name="Test Warehouse",
            administrator_id="admin123",
            status="active"
        )
        
        # Mock the repository
        mock_repository = MagicMock(spec=WarehouseRepository)
        mock_repository.get_by_id.return_value = existing_warehouse  # Warehouse exists
        mock_repository.delete.return_value = False  # Deletion failed
        
        # Create the use case with the mocked repository
        use_case = DeleteWarehouse(mock_repository)
        
        # Act
        result = use_case.execute(warehouse_id)
        
        # Assert
        mock_repository.get_by_id.assert_called_once_with(warehouse_id)
        mock_repository.delete.assert_called_once_with(warehouse_id)
        assert result is False

    def test_execute_warehouse_not_found(self):
        """Test execution of DeleteWarehouse use case when warehouse is not found"""
        # Arrange
        warehouse_id = "nonexistent"
        
        # Mock the repository
        mock_repository = MagicMock(spec=WarehouseRepository)
        mock_repository.get_by_id.return_value = None  # Warehouse doesn't exist
        
        # Create the use case with the mocked repository
        use_case = DeleteWarehouse(mock_repository)
        
        # Act & Assert
        with pytest.raises(ResourceNotFoundError):
            use_case.execute(warehouse_id)
        
        mock_repository.get_by_id.assert_called_once_with(warehouse_id)
        mock_repository.delete.assert_not_called()