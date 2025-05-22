import pytest
from datetime import datetime
import uuid
from unittest.mock import Mock

from src.infrastructure.mapper.recommendation_result_mapper import RecommendationResultMapper
from src.infrastructure.model.recommendation_result_model import RecommendationResultModel
from src.domain.entities.recommentation_result_dto import RecommendationResultDTO


class TestRecommendationResultMapper:

    @pytest.fixture
    def sample_model(self):
        """Create a sample RecommendationResultModel for testing"""
        test_id = uuid.uuid4()
        return RecommendationResultModel(
            id=test_id,
            product_id="PROD-123",
            events={"event1": "data1", "event2": "data2"},
            target_sales_amount=1500.0,
            currency="USD",
            recommendation="Buy 100 units",
            created_at=datetime(2023, 5, 15, 10, 30, 0)
        )

    @pytest.fixture
    def sample_dto(self):
        """Create a sample RecommendationResultDTO for testing"""
        test_id = str(uuid.uuid4())
        return RecommendationResultDTO(
            id=test_id,
            product_id="PROD-123",
            events={"event1": "data1", "event2": "data2"},
            target_sales_amount=1500.0,
            currency="USD",
            recommendation="Buy 100 units",
            created_at="2023-05-15T10:30:00"
        )

    def test_to_dto(self, sample_model):
        """Test converting from model to DTO"""
        # Act
        result = RecommendationResultMapper.to_dto(sample_model)

        # Assert
        assert isinstance(result, RecommendationResultDTO)
        assert str(sample_model.id) == result.id
        assert sample_model.product_id == result.product_id
        assert sample_model.events == result.events
        assert sample_model.target_sales_amount == result.target_sales_amount
        assert sample_model.currency == result.currency
        assert sample_model.recommendation == result.recommendation
        assert sample_model.created_at.isoformat() == result.created_at

    def test_to_dto_with_none_created_at(self):
        """Test converting from model to DTO when created_at is None"""
        # Arrange
        test_id = uuid.uuid4()
        model = RecommendationResultModel(
            id=test_id,
            product_id="PROD-123",
            events={"event1": "data1"},
            target_sales_amount=1500.0,
            currency="USD",
            recommendation="Buy 100 units",
            created_at=None
        )

        # Act
        result = RecommendationResultMapper.to_dto(model)

        # Assert
        assert result.created_at is None

    def test_to_model(self, sample_dto):
        """Test converting from DTO to model"""
        # Act
        result = RecommendationResultMapper.to_model(sample_dto)

        # Assert
        assert isinstance(result, RecommendationResultModel)
        assert sample_dto.id == result.id
        assert sample_dto.product_id == result.product_id
        assert sample_dto.events == result.events
        assert sample_dto.target_sales_amount == result.target_sales_amount
        assert sample_dto.currency == result.currency
        assert sample_dto.recommendation == result.recommendation
        assert sample_dto.created_at == result.created_at

    def test_to_dto_list(self, sample_model):
        """Test converting a list of models to a list of DTOs"""
        # Arrange
        models = [sample_model, sample_model]

        # Act
        result = RecommendationResultMapper.to_dto_list(models)

        # Assert
        assert isinstance(result, list)
        assert len(result) == 2

        for dto in result:
            assert isinstance(dto, RecommendationResultDTO)
            assert str(sample_model.id) == dto.id
            assert sample_model.product_id == dto.product_id
            assert sample_model.events == dto.events
            assert sample_model.target_sales_amount == dto.target_sales_amount
            assert sample_model.currency == dto.currency
            assert sample_model.recommendation == dto.recommendation
            assert sample_model.created_at.isoformat() == dto.created_at

    def test_to_dto_list_empty(self):
        """Test converting an empty list of models"""
        # Arrange
        models = []

        # Act
        result = RecommendationResultMapper.to_dto_list(models)

        # Assert
        assert isinstance(result, list)
        assert len(result) == 0