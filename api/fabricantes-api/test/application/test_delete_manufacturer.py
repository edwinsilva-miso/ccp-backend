import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.domain.entities.manufacturer_dto import ManufacturerDTO
from src.application.delete_manufacturer import DeleteManufacturer
from src.application.errors.errors import ManufacturerNotExistsError
from src.infrastructure.adapters.manufacturer_adapter import ManufacturerAdapter

class TestDeleteManufacturer:
    @pytest.fixture
    def manufacturer_repository_mock(self):
        return Mock(spec=ManufacturerAdapter)

    @pytest.fixture
    def delete_manufacturer_usecase(self, manufacturer_repository_mock):
        return DeleteManufacturer(manufacturer_repository_mock)

    @pytest.fixture
    def existing_manufacturer(self):
        return ManufacturerDTO(
            id="test-id-123",
            name="Test Manufacturer",
            nit="1234567890",
            address="123 Test St.",
            phone="123-456-7890",
            email="test@example.com",
            legal_representative="Test Rep",
            country="Test Country",
            status="ACTIVO",
            created=datetime.now().isoformat(),
            updated=datetime.now().isoformat()
        )

    @pytest.fixture(autouse=True)
    def teardown_method(self):
        """Clean up resources after each test method"""
        yield
        patch.stopall()

    def test_execute_deletes_manufacturer_successfully(self, delete_manufacturer_usecase,
                                                      manufacturer_repository_mock,
                                                      existing_manufacturer):
        # Arrange
        manufacturer_id = existing_manufacturer.id
        manufacturer_repository_mock.get_by_id.return_value = existing_manufacturer

        # Act
        delete_manufacturer_usecase.execute(manufacturer_id)

        # Assert
        manufacturer_repository_mock.get_by_id.assert_called_once_with(manufacturer_id)
        manufacturer_repository_mock.delete.assert_called_once_with(manufacturer_id)

    def test_execute_raises_error_for_nonexistent_manufacturer(self, delete_manufacturer_usecase,
                                                              manufacturer_repository_mock):
        # Arrange
        manufacturer_id = "nonexistent-id"
        manufacturer_repository_mock.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ManufacturerNotExistsError):
            delete_manufacturer_usecase.execute(manufacturer_id)

        manufacturer_repository_mock.get_by_id.assert_called_once_with(manufacturer_id)
        manufacturer_repository_mock.delete.assert_not_called()


    def test_execute_with_empty_id(self, delete_manufacturer_usecase, manufacturer_repository_mock):
        # Arrange
        manufacturer_id = ""
        manufacturer_repository_mock.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ManufacturerNotExistsError):
            delete_manufacturer_usecase.execute(manufacturer_id)