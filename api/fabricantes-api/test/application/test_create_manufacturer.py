import uuid
from unittest.mock import Mock

import pytest
from src.application.create_manufacturer import CreateManufacturer
from src.application.errors.errors import InvalidFormatError, ManufacturerAlreadyExistsError
from src.domain.entities.manufacturer_dto import ManufacturerDTO
from src.infrastructure.adapters.manufacturer_adapter import ManufacturerAdapter


class TestCreateManufacturer:
    @pytest.fixture
    def manufacturer_repository_mock(self):
        return Mock(spec=ManufacturerAdapter)

    @pytest.fixture
    def create_manufacturer_usecase(self, manufacturer_repository_mock):
        return CreateManufacturer(manufacturer_repository_mock)

    @pytest.fixture
    def valid_manufacturer_data(self):
        return {
            "id": None,
            "name": "Test Manufacturer",
            "nit": "123456789-0",
            "address": "123 Test St.",
            "phone": "123-456-7890",
            "email": "test@example.com",
            "legal_representative": "Test Rep",
            "country": "Test Country",
            "status": None,
            "created": None,
            "updated": None
        }


    def test_execute_creates_manufacturer_successfully(self, create_manufacturer_usecase, manufacturer_repository_mock,
                                                       valid_manufacturer_data):
        # Arrange
        manufacturer_id = str(uuid.uuid4())
        manufacturer_dto = ManufacturerDTO(**valid_manufacturer_data)

        # Mock repository checks
        manufacturer_repository_mock.get_by_nit.return_value = None
        manufacturer_repository_mock.add.return_value = manufacturer_id

        # Act
        result = create_manufacturer_usecase.execute(manufacturer_dto)

        # Assert
        assert result is not None
        assert result == manufacturer_id

        # Verify repository was called with correct data
        manufacturer_repository_mock.get_by_nit.assert_called_once_with(manufacturer_dto.nit)
        manufacturer_repository_mock.add.assert_called_once()



    def test_execute_validates_email_format(self, create_manufacturer_usecase):
        # Arrange
        invalid_data = ManufacturerDTO(
            id=None,
            name="Test Manufacturer",
            nit="123456789-0",
            address="123 Test St.",
            phone="123-456-7890",
            email="invalid-email",
            legal_representative="Test Rep",
            country="Test Country",
            status=None,
            created=None,
            updated=None
        )

        # Act & Assert
        with pytest.raises(InvalidFormatError):
            create_manufacturer_usecase.execute(invalid_data)

    def test_execute_validates_nit_format(self, create_manufacturer_usecase):
        # Arrange
        invalid_data = ManufacturerDTO(
            id=None,
            name="Test Manufacturer",
            nit="ABC13",
            address="123 Test St.",
            phone="123-456-7890",
            email="mail@example.net",
            legal_representative="Test Rep",
            country="Test Country",
            status=None,
            created=None,
            updated=None
        )

        # Act & Assert
        with pytest.raises(InvalidFormatError):
            create_manufacturer_usecase.execute(invalid_data)

    def test_execute_validates_manufacturer_existence(self, create_manufacturer_usecase, manufacturer_repository_mock):
        # Arrange
        manufacturer_repository_mock.get_by_nit.return_value = True
        data = ManufacturerDTO(
            id=None,
            name="Test Manufacturer",
            nit="123456789-0",
            address="123 Test St.",
            phone="123-456-7890",
            email="email@mail.net",
            legal_representative="Test Rep",
            country="Test Country",
            status=None,
            created=None,
            updated=None
        )

        # Act & Assert
        with pytest.raises(ManufacturerAlreadyExistsError):
            create_manufacturer_usecase.execute(data)