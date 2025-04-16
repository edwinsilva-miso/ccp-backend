import uuid

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.domain.entities.manufacturer_dto import ManufacturerDTO
from src.application.update_manufacturer import UpdateManufacturer
from src.application.errors.errors import ManufacturerNotExistsError, InvalidFormatError


class TestUpdateManufacturer:
    @pytest.fixture
    def manufacturer_repository_mock(self):
        return Mock()

    @pytest.fixture
    def update_manufacturer_usecase(self, manufacturer_repository_mock):
        return UpdateManufacturer(manufacturer_repository_mock)

    @pytest.fixture
    def existing_manufacturer(self):
        return ManufacturerDTO(
            id="test-id-123",
            name="Original Manufacturer",
            nit="1234567890",
            address="123 Original St.",
            phone="123-456-7890",
            email="original@example.com",
            legal_representative="Original Rep",
            country="Original Country",
            status="ACTIVO",
            created=datetime.now().isoformat(),
            updated=datetime.now().isoformat()
        )

    @pytest.fixture
    def updated_manufacturer_data(self):
        return ManufacturerDTO(
            id="test-id-123",
            name="Updated Manufacturer",
            nit="0987654321",
            address="456 Updated St.",
            phone="098-765-4321",
            email="updated@example.com",
            legal_representative="Updated Rep",
            country="Updated Country",
            status="ACTIVO",
            created=None,
            updated=None
        )

    @pytest.fixture(autouse=True)
    def teardown_method(self):
        """Clean up resources after each test method"""
        yield
        patch.stopall()

    def test_update_manufacturer_successfully(self, update_manufacturer_usecase,
                                              manufacturer_repository_mock,
                                              existing_manufacturer,
                                              updated_manufacturer_data):
        # Arrange
        manufacturer_repository_mock.get_by_id.return_value = existing_manufacturer
        manufacturer_repository_mock.update.return_value = updated_manufacturer_data
        manufacturer_id = existing_manufacturer.id

        # Act
        result = update_manufacturer_usecase.execute(manufacturer_id, updated_manufacturer_data)

        # Assert
        assert result is not None
        assert result.id == updated_manufacturer_data.id
        assert result.name == updated_manufacturer_data.name
        assert result.nit == updated_manufacturer_data.nit
        assert result.address == updated_manufacturer_data.address
        assert result.phone == updated_manufacturer_data.phone
        assert result.email == updated_manufacturer_data.email
        assert result.legal_representative == updated_manufacturer_data.legal_representative
        assert result.country == updated_manufacturer_data.country

        manufacturer_repository_mock.get_by_id.assert_called_once_with(manufacturer_id)
        manufacturer_repository_mock.update.assert_called_once()

    def test_update_nonexistent_manufacturer(self, update_manufacturer_usecase,
                                             manufacturer_repository_mock,
                                             updated_manufacturer_data):
        # Arrange
        manufacturer_id = updated_manufacturer_data.id
        manufacturer_repository_mock.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ManufacturerNotExistsError):
            update_manufacturer_usecase.execute(manufacturer_id, updated_manufacturer_data)

        manufacturer_repository_mock.get_by_id.assert_called_once_with(manufacturer_id)
        manufacturer_repository_mock.update.assert_not_called()

    def test_update_manufacturer_with_invalid_email(self, update_manufacturer_usecase,
                                                    manufacturer_repository_mock,
                                                    existing_manufacturer):
        # Arrange
        manufacturer_id = existing_manufacturer.id
        invalid_data = ManufacturerDTO(
            id=existing_manufacturer.id,
            name="Valid Name",
            email="invalid-email",  # Invalid email format
            nit="1234567890",
            address="123 Test St.",
            phone="123-456-7890",
            legal_representative="Test Rep",
            country="Test Country",
            status="ACTIVO",
            created=None,
            updated=None
        )

        manufacturer_repository_mock.get_by_id.return_value = existing_manufacturer

        # Act & Assert
        with pytest.raises(InvalidFormatError):
            update_manufacturer_usecase.execute(manufacturer_id, invalid_data)

        manufacturer_repository_mock.update.assert_not_called()

    def test_update_only_specific_fields(self, update_manufacturer_usecase,
                                         manufacturer_repository_mock,
                                         existing_manufacturer):
        # Arrange
        partial_update = ManufacturerDTO(
            id=existing_manufacturer.id,
            name="Updated Name Only",
            email="info@test.dev",
            nit=None,  # Should keep existing value
            address=None,
            phone=None,
            legal_representative=None,
            country=None,
            status=None,
            created=None,
            updated=None
        )

        expected_result = ManufacturerDTO(
            id=existing_manufacturer.id,
            name="Updated Name Only",
            email=existing_manufacturer.email,
            nit=existing_manufacturer.nit,
            address=existing_manufacturer.address,
            phone=existing_manufacturer.phone,
            legal_representative=existing_manufacturer.legal_representative,
            country=existing_manufacturer.country,
            status=existing_manufacturer.status,
            created=existing_manufacturer.created,
            updated=datetime.now().isoformat()
        )
        manufacturer_id = existing_manufacturer.id

        manufacturer_repository_mock.get_by_id.return_value = existing_manufacturer
        manufacturer_repository_mock.update.return_value = expected_result

        # Act
        result = update_manufacturer_usecase.execute(manufacturer_id, partial_update)

        # Assert
        assert result is not None
        assert result.id == existing_manufacturer.id
        assert result.name == "Updated Name Only"
        assert result.email == existing_manufacturer.email  # Should be unchanged
        assert result.nit == existing_manufacturer.nit  # Should be unchanged

        manufacturer_repository_mock.get_by_id.assert_called_once_with(manufacturer_id)
        manufacturer_repository_mock.update.assert_called_once()

