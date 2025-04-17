import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.domain.entities.manufacturer_dto import ManufacturerDTO
from src.application.get_manufacturer_by_nit import GetManufacturerByNit
from src.application.errors.errors import ManufacturerNotExistsError


class TestGetManufacturerByNit:
    @pytest.fixture
    def manufacturer_repository_mock(self):
        return Mock()

    @pytest.fixture
    def get_manufacturer_by_nit_usecase(self, manufacturer_repository_mock):
        return GetManufacturerByNit(manufacturer_repository_mock)

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

    def test_get_manufacturer_by_nit_successfully(self, get_manufacturer_by_nit_usecase,
                                                manufacturer_repository_mock,
                                                existing_manufacturer):
        # Arrange
        nit = existing_manufacturer.nit
        manufacturer_repository_mock.get_by_nit.return_value = existing_manufacturer

        # Act
        result = get_manufacturer_by_nit_usecase.execute(nit)

        # Assert
        assert result is not None
        assert result.id == existing_manufacturer.id
        assert result.name == existing_manufacturer.name
        assert result.nit == existing_manufacturer.nit
        assert result.address == existing_manufacturer.address
        assert result.phone == existing_manufacturer.phone
        assert result.email == existing_manufacturer.email
        assert result.legal_representative == existing_manufacturer.legal_representative
        assert result.country == existing_manufacturer.country
        assert result.status == existing_manufacturer.status

        manufacturer_repository_mock.get_by_nit.assert_called_once_with(nit)

    def test_get_nonexistent_manufacturer_by_nit(self, get_manufacturer_by_nit_usecase,
                                               manufacturer_repository_mock):
        # Arrange
        nit = "nonexistent-nit"
        manufacturer_repository_mock.get_by_nit.return_value = None

        # Act & Assert
        with pytest.raises(ManufacturerNotExistsError):
            get_manufacturer_by_nit_usecase.execute(nit)

        manufacturer_repository_mock.get_by_nit.assert_called_once_with(nit)

    def test_get_manufacturer_with_empty_nit(self, get_manufacturer_by_nit_usecase,
                                           manufacturer_repository_mock):
        # Arrange
        nit = ""
        manufacturer_repository_mock.get_by_nit.return_value = None

        # Act & Assert
        with pytest.raises(ManufacturerNotExistsError):
            get_manufacturer_by_nit_usecase.execute(nit)

        manufacturer_repository_mock.get_by_nit.assert_called_once_with(nit)
