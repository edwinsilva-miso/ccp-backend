import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.domain.entities.manufacturer_dto import ManufacturerDTO
from src.application.get_all_manufacturers import GetAllManufacturers


class TestGetAllManufacturers:
    @pytest.fixture
    def manufacturer_repository_mock(self):
        return Mock()

    @pytest.fixture
    def get_all_manufacturers_usecase(self, manufacturer_repository_mock):
        return GetAllManufacturers(manufacturer_repository_mock)

    @pytest.fixture
    def sample_manufacturers(self):
        return [
            ManufacturerDTO(
                id="test-id-1",
                name="Manufacturer 1",
                nit="1111111111",
                address="123 First St.",
                phone="111-111-1111",
                email="first@example.com",
                legal_representative="Rep One",
                country="Country One",
                status="ACTIVO",
                created=datetime.now().isoformat(),
                updated=datetime.now().isoformat()
            ),
            ManufacturerDTO(
                id="test-id-2",
                name="Manufacturer 2",
                nit="2222222222",
                address="456 Second St.",
                phone="222-222-2222",
                email="second@example.com",
                legal_representative="Rep Two",
                country="Country Two",
                status="ACTIVO",
                created=datetime.now().isoformat(),
                updated=datetime.now().isoformat()
            ),
            ManufacturerDTO(
                id="test-id-3",
                name="Manufacturer 3",
                nit="3333333333",
                address="789 Third St.",
                phone="333-333-3333",
                email="third@example.com",
                legal_representative="Rep Three",
                country="Country Three",
                status="INACTIVO",
                created=datetime.now().isoformat(),
                updated=datetime.now().isoformat()
            )
        ]

    @pytest.fixture(autouse=True)
    def teardown_method(self):
        """Clean up resources after each test method"""
        yield
        patch.stopall()

    def test_get_all_manufacturers_successfully(self, get_all_manufacturers_usecase,
                                                manufacturer_repository_mock,
                                                sample_manufacturers):
        # Arrange
        manufacturer_repository_mock.get_all.return_value = sample_manufacturers

        # Act
        result = get_all_manufacturers_usecase.execute()

        # Assert
        assert result is not None
        assert len(result) == 3

        # Verify all manufacturers are returned correctly
        for i, manufacturer in enumerate(result):
            assert manufacturer.id == sample_manufacturers[i].id
            assert manufacturer.name == sample_manufacturers[i].name
            assert manufacturer.nit == sample_manufacturers[i].nit
            assert manufacturer.status == sample_manufacturers[i].status

        manufacturer_repository_mock.get_all.assert_called_once()

    def test_get_all_returns_empty_list(self, get_all_manufacturers_usecase,
                                        manufacturer_repository_mock):
        # Arrange
        manufacturer_repository_mock.get_all.return_value = []

        # Act
        result = get_all_manufacturers_usecase.execute()

        # Assert
        assert result is not None
        assert len(result) == 0
        assert isinstance(result, list)

        manufacturer_repository_mock.get_all.assert_called_once()

    def test_get_all_handles_repository_errors(self, get_all_manufacturers_usecase,
                                               manufacturer_repository_mock):
        # Arrange
        manufacturer_repository_mock.get_all.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            get_all_manufacturers_usecase.execute()

        manufacturer_repository_mock.get_all.assert_called_once()
