import json
import pytest
import uuid
from datetime import datetime

from src.infrastructure.mapper.product_mapper import ProductMapper
from src.domain.entities.product_dto import ProductDTO
from src.infrastructure.model.product_model import ProductModel


class TestProductMapper:
    @pytest.fixture
    def sample_uuid(self):
        return uuid.uuid4()

    @pytest.fixture
    def manufacturer_uuid(self):
        return uuid.uuid4()

    @pytest.fixture
    def current_datetime(self):
        return datetime.utcnow()

    @pytest.fixture
    def product_dto(self, sample_uuid, manufacturer_uuid, current_datetime):
        return ProductDTO(
            id=sample_uuid,
            manufacturer_id=manufacturer_uuid,
            name="Test Product",
            brand="Test Brand",
            currency="USD",
            description="Test description",
            stock=100,
            details={"weight": "500g", "dimensions": "10x20x30cm"},
            storage_conditions="Store in a cool place",
            price=29.99,
            delivery_time=5,
            #images=[{"url": "image1.jpg", "is_primary": True}, {"url": "image2.jpg", "is_primary": False}],
            images=["image1.jpg", "image2.jpg"],
            created_at=current_datetime.isoformat(),
            updated_at=current_datetime.isoformat()
        )

    @pytest.fixture
    def product_model(self, sample_uuid, manufacturer_uuid, current_datetime):
        return ProductModel(
            id=sample_uuid,
            manufacturer_id=manufacturer_uuid,
            name="Test Product",
            brand="Test Brand",
            currency="USD",
            description="Test description",
            stock=100,
            details=json.dumps({"weight": "500g", "dimensions": "10x20x30cm"}),
            storage_conditions="Store in a cool place",
            price=29.99,
            delivery_time=5,
            # images=[{"url": "image1.jpg", "is_primary": True}, {"url": "image2.jpg", "is_primary": False}],
            images=["image1.jpg", "image2.jpg"],
            createdAt=current_datetime,
            updatedAt=current_datetime
        )

    def test_to_domain_with_valid_dto(self, product_dto):
        # Act
        product_model = ProductMapper.to_domain(product_dto)

        # Assert
        assert product_model.id == product_dto.id
        assert product_model.name == product_dto.name
        assert product_model.brand == product_dto.brand
        assert product_model.description == product_dto.description
        assert product_model.stock == product_dto.stock
        assert product_model.details == json.dumps(product_dto.details)  # String representation
        assert product_model.storage_conditions == product_dto.storage_conditions
        assert product_model.price == product_dto.price
        assert product_model.delivery_time == product_dto.delivery_time
        assert product_model.images == product_dto.images  # JSON column handles this automatically
        assert product_model.manufacturer_id == product_dto.manufacturer_id

    def test_to_domain_with_none(self):
        # Act
        result = ProductMapper.to_domain(None)

        # Assert
        assert result is None

    def test_to_dto_with_valid_model(self, product_model):
        # Act
        product_dto = ProductMapper.to_dto(product_model)

        # Assert
        assert product_dto.id == product_model.id
        assert product_dto.name == product_model.name
        assert product_dto.brand == product_model.brand
        assert product_dto.description == product_model.description
        assert product_dto.stock == product_model.stock
        assert product_dto.details == json.loads(product_model.details)  # Dict representation
        assert product_dto.storage_conditions == product_model.storage_conditions
        assert product_dto.price == product_model.price
        assert product_dto.delivery_time == product_model.delivery_time
        assert product_dto.images == product_model.images
        assert product_dto.manufacturer_id == product_model.manufacturer_id
        assert product_dto.created_at == product_model.createdAt.isoformat()
        assert product_dto.updated_at == product_model.updatedAt.isoformat()

    def test_to_dto_with_none(self):
        # Act
        result = ProductMapper.to_dto(None)

        # Assert
        assert result is None

    def test_to_dto_list(self, product_model):
        # Arrange
        models = [product_model, product_model]

        # Act
        dtos = ProductMapper.to_dto_list(models)

        # Assert
        assert len(dtos) == 2
        for dto in dtos:
            assert isinstance(dto, ProductDTO)
            assert dto.id == product_model.id

    def test_to_domain_list(self, product_dto):
        # Arrange
        dtos = [product_dto, product_dto]

        # Act
        models = ProductMapper.to_domain_list(dtos)

        # Assert
        assert len(models) == 2
        for model in models:
            assert isinstance(model, ProductModel)
            assert model.id == product_dto.id
            assert model.details == json.dumps(product_dto.details)

    def test_with_null_details(self, product_dto, product_model):
        # Arrange
        product_dto.details = None
        product_model.details = None

        # Act
        model = ProductMapper.to_domain(product_dto)
        dto = ProductMapper.to_dto(product_model)

        # Assert
        assert model.details is None
        assert dto.details is None