import pytest
from datetime import datetime, timezone
from src.domain.entities.manufacturer_dto import ManufacturerDTO
from src.infrastructure.model.manufacturer_model import ManufacturerModel, StatusEnum
from src.infrastructure.mapper.manufacturer_mapper import ManufacturerMapper


class TestManufacturerMapper:

    def test_to_dto_complete_mapping(self):
        # Arrange
        model = ManufacturerModel(
            id="test-id-123",
            name="Test Manufacturer",
            address="123 Test St.",
            phone="123-456-7890",
            email="test@example.com",
            legal_representative="Test Rep",
            country="Test Country",
            status=StatusEnum.ACTIVO,  # ACTIVE
            nit="1234567890",
            createdAt=datetime(2023, 1, 1, tzinfo=timezone.utc),
            updatedAt=datetime(2023, 1, 2, tzinfo=timezone.utc)
        )

        # Act
        dto = ManufacturerMapper.to_dto(model)

        # Assert
        assert isinstance(dto, ManufacturerDTO)
        assert dto.id == "test-id-123"
        assert dto.name == "Test Manufacturer"
        assert dto.address == "123 Test St."
        assert dto.phone == "123-456-7890"
        assert dto.email == "test@example.com"
        assert dto.legal_representative == "Test Rep"
        assert dto.country == "Test Country"
        assert dto.status == "ACTIVO"
        assert dto.nit == "1234567890"
        assert dto.created == datetime(2023, 1, 1, tzinfo=timezone.utc).isoformat()
        assert dto.updated == datetime(2023, 1, 2, tzinfo=timezone.utc).isoformat()

    def test_to_dto_with_inactive_status(self):
        # Arrange
        model = ManufacturerModel(
            id="test-id-123",
            name="Test Manufacturer",
            status=StatusEnum.INACTIVO,  # INACTIVE
            createdAt=datetime(2023, 1, 1, tzinfo=timezone.utc),
            updatedAt=datetime(2023, 1, 2, tzinfo=timezone.utc)
        )

        # Act
        dto = ManufacturerMapper.to_dto(model)

        # Assert
        assert dto.status == "INACTIVO"

    def test_to_domain_complete_mapping(self):
        # Arrange
        dto = ManufacturerDTO(
            id="test-id-123",
            name="Test Manufacturer",
            address="123 Test St.",
            phone="123-456-7890",
            email="test@example.com",
            legal_representative="Test Rep",
            country="Test Country",
            status="ACTIVO", # ACTIVE
            nit="1234567890",
            created=datetime(2023, 1, 1, tzinfo=timezone.utc),
            updated=datetime(2023, 1, 2, tzinfo=timezone.utc)
        )

        # Act
        model = ManufacturerMapper.to_domain(dto)

        # Assert
        assert isinstance(model, ManufacturerModel)
        assert model.id == "test-id-123"
        assert model.name == "Test Manufacturer"
        assert model.address == "123 Test St."
        assert model.phone == "123-456-7890"
        assert model.email == "test@example.com"
        assert model.legal_representative == "Test Rep"
        assert model.country == "Test Country"
        assert model.status == StatusEnum.ACTIVO.name  # ACTIVE
        assert model.nit == "1234567890"
        assert model.createdAt == datetime(2023, 1, 1, tzinfo=timezone.utc)
        assert model.updatedAt == datetime(2023, 1, 2, tzinfo=timezone.utc)

    def test_to_domain_with_inactive_status(self):
        # Arrange
        dto = ManufacturerDTO(
            id="test-id-123",
            nit=None,
            name="Test Manufacturer",
            address=None,
            phone=None,
            email=None,
            legal_representative=None,
            country=None,
            status="INACTIVO",
            created=datetime(2023, 1, 1, tzinfo=timezone.utc),
            updated=datetime(2023, 1, 2, tzinfo=timezone.utc)
        )

        # Act
        model = ManufacturerMapper.to_domain(dto)

        # Assert
        assert model.status == StatusEnum.INACTIVO.name  # INACTIVE

    def test_to_dto_with_none_fields(self):
        # Arrange
        model = ManufacturerModel(
            id="test-id-123",
            nit=None,
            name="Test Manufacturer",
            address=None,
            phone=None,
            email=None,
            legal_representative=None,
            country=None,
            status=StatusEnum.ACTIVO,  # ACTIVE
            createdAt=datetime(2023, 1, 1, tzinfo=timezone.utc),
            updatedAt=datetime(2023, 1, 2, tzinfo=timezone.utc)
        )

        # Act
        entity = ManufacturerMapper.to_dto(model)

        # Assert
        assert entity.address is None
        assert entity.phone is None
        assert entity.email is None
        assert entity.legal_representative is None
        assert entity.country is None
        assert entity.nit is None

    def test_to_domain_with_none_fields(self):
        # Arrange
        dto = ManufacturerDTO(
            id="test-id-123",
            nit=None,
            name="Test Manufacturer",
            address=None,
            phone=None,
            email=None,
            legal_representative=None,
            country=None,
            status="ACTIVO",  # ACTIVE
            created=datetime(2023, 1, 1, tzinfo=timezone.utc),
            updated=datetime(2023, 1, 2, tzinfo=timezone.utc)
        )

        # Act
        model = ManufacturerMapper.to_domain(dto)

        # Assert
        assert model.address is None
        assert model.phone is None
        assert model.email is None
        assert model.legal_representative is None
        assert model.country is None
        assert model.nit is None

    def test_to_dto_with_none(self):
        # Act
        dto = ManufacturerMapper.to_dto(None)

        # Assert
        assert dto is None

    def test_to_domain_with_none(self):
        # Act
        model = ManufacturerMapper.to_domain(None)

        # Assert
        assert model is None

    def test_to_domain_list(self):
        # Arrange
        dto = ManufacturerDTO(
            id="test-id-123",
            nit=None,
            name="Test Manufacturer",
            address=None,
            phone=None,
            email=None,
            legal_representative=None,
            country=None,
            status="ACTIVO",  # ACTIVE
            created=datetime(2023, 1, 1, tzinfo=timezone.utc),
            updated=datetime(2023, 1, 2, tzinfo=timezone.utc)
        )

        dto_list = [dto, dto]

        # Act
        model = ManufacturerMapper.to_domain_list(dto_list)

        # Assert
        assert isinstance(model, list)
        assert len(model) == 2
        assert isinstance(model[0], ManufacturerModel)
        assert model[0].id == "test-id-123"
        assert model[1].id == "test-id-123"
        assert model[0].name == "Test Manufacturer"
        assert model[1].name == "Test Manufacturer"
        assert model[0].status == StatusEnum.ACTIVO.name
        assert model[1].status == StatusEnum.ACTIVO.name

    def test_to_dto_list(self):
        model = ManufacturerModel(
            id="test-id-123",
            name="Test Manufacturer",
            address="123 Test St.",
            phone="123-456-7890",
            email="test@example.com",
            legal_representative="Test Rep",
            country="Test Country",
            status=StatusEnum.ACTIVO,  # ACTIVE
            nit="1234567890",
            createdAt=datetime(2023, 1, 1, tzinfo=timezone.utc),
            updatedAt=datetime(2023, 1, 2, tzinfo=timezone.utc)
        )

        model_list = [model]

        # Act
        dto = ManufacturerMapper.to_dto_list(model_list)

        # Assert
        assert isinstance(dto, list)
        assert len(dto) == 1
        assert isinstance(dto[0], ManufacturerDTO)
        assert dto[0].id == "test-id-123"
        assert dto[0].name == "Test Manufacturer"
        assert dto[0].address == "123 Test St."
        assert dto[0].phone == "123-456-7890"
        assert dto[0].email == "test@example.com"
        assert dto[0].legal_representative == "Test Rep"
        assert dto[0].country == "Test Country"
        assert dto[0].status == "ACTIVO"
        assert dto[0].nit == "1234567890"
        assert dto[0].created == datetime(2023, 1, 1, tzinfo=timezone.utc).isoformat()
        assert dto[0].updated == datetime(2023, 1, 2, tzinfo=timezone.utc).isoformat()

