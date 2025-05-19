import json
from unittest.mock import Mock, patch

import pytest
from src.application.make_recommendation import MakeRecommendation
from src.domain.entities.recommentation_result_dto import RecommendationResultDTO


class TestMakeRecommendation:

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository for testing"""
        return Mock()

    @pytest.fixture
    def mock_calculation_service(self):
        """Create a mock calculation service for testing"""
        return Mock()

    @pytest.fixture
    def make_recommendation_service(self, mock_repository):
        """Create an instance of MakeRecommendation for testing"""
        service = MakeRecommendation(mock_repository)
        # Replace the real calculation service with a mock
        service.calculation_sales_service = Mock()
        return service

    @pytest.fixture
    def sample_sales_data(self):
        """Create sample sales data for testing"""
        return {
            'product': {
                'id': 'PROD-123',
                'name': 'Test Product',
                'stock': 50
            },
            'projection': {
                'salesTarget': 200,
                'currency': 'USD'
            },
            'events': [
                {'date': '2023-05-30', 'name': 'Sale Event'}
            ],
            'manufacturer': {
                'name': 'Test Manufacturer'
            }
        }

    @pytest.fixture
    def expected_recommendation_text(self):
        """Create the expected recommendation text"""
        return "La cantidad óptima a comprar para Test Product y obtener $200 USD es 150 unidades."

    def test_execute_creates_dto_correctly(self, make_recommendation_service, sample_sales_data, mock_repository):
        """Test that execute creates the DTO with correct values"""
        # Arrange
        make_recommendation_service.calculation_sales_service.calculate_optimum_quantity.return_value = 150

        # Mock the repository.add method to return a saved DTO
        saved_dto = RecommendationResultDTO(
            id="1",
            product_id=sample_sales_data['product']['id'],
            events=json.dumps(sample_sales_data['events']),
            target_sales_amount=sample_sales_data['projection']['salesTarget'],
            currency=sample_sales_data['projection']['currency'],
            recommendation="La cantidad óptima a comprar para Test Product y obtener $200 USD es 150 unidades.",
            created_at="2023-05-15T10:30:00"
        )
        mock_repository.add.return_value = saved_dto

        # Act
        result = make_recommendation_service.execute(sample_sales_data)

        # Assert
        assert isinstance(result, RecommendationResultDTO)
        assert result.product_id == sample_sales_data['product']['id']
        assert result.target_sales_amount == sample_sales_data['projection']['salesTarget']
        assert result.currency == sample_sales_data['projection']['currency']
        assert "La cantidad óptima a comprar para Test Product y obtener $200 USD es 150 unidades." in result.recommendation

    def test_execute_calls_calculation_service(self, make_recommendation_service, sample_sales_data, mock_repository):
        """Test that the calculation service is called with the correct data"""
        # Arrange
        make_recommendation_service.calculation_sales_service.calculate_optimum_quantity.return_value = 150
        mock_repository.add.return_value = Mock(spec=RecommendationResultDTO)

        # Act
        make_recommendation_service.execute(sample_sales_data)

        # Assert
        make_recommendation_service.calculation_sales_service.calculate_optimum_quantity.assert_called_once_with(
            sample_sales_data)

    def test_execute_saves_recommendation(self, make_recommendation_service, sample_sales_data, mock_repository,
                                          expected_recommendation_text):
        """Test that the recommendation is saved to the repository"""
        # Arrange
        make_recommendation_service.calculation_sales_service.calculate_optimum_quantity.return_value = 150
        mock_repository.add.return_value = Mock(spec=RecommendationResultDTO)

        # Act
        make_recommendation_service.execute(sample_sales_data)

        # Assert
        mock_repository.add.assert_called_once()
        # Check the DTO passed to repository.add has the correct values
        dto_arg = mock_repository.add.call_args[0][0]
        assert dto_arg.product_id == sample_sales_data['product']['id']
        assert dto_arg.target_sales_amount == sample_sales_data['projection']['salesTarget']
        assert dto_arg.currency == sample_sales_data['projection']['currency']
        assert expected_recommendation_text in dto_arg.recommendation

    @patch('src.application.make_recommendation.logger')
    def test_execute_logs_correctly(self, mock_logger, make_recommendation_service, sample_sales_data, mock_repository):
        """Test that the execute method logs correctly"""
        # Arrange
        make_recommendation_service.calculation_sales_service.calculate_optimum_quantity.return_value = 150
        mock_repository.add.return_value = Mock(spec=RecommendationResultDTO)

        # Act
        make_recommendation_service.execute(sample_sales_data)

        # Assert
        mock_logger.debug.assert_any_call("Starting the recommendation process")
        mock_logger.debug.assert_any_call("Optimum quantity calculated: %d", 150)
        mock_logger.info.assert_called_with("Recommendation process completed successfully")

    def test_execute_handles_missing_data(self, make_recommendation_service, mock_repository):
        """Test that execute handles missing data gracefully"""
        # Arrange
        incomplete_data = {
            'product': {'id': 'PROD-123', 'name': 'Test Product'},
            'manufacturer': {'name': 'Test Manufacturer'},
            'projection': {}
        }
        make_recommendation_service.calculation_sales_service.calculate_optimum_quantity.return_value = 0
        mock_repository.add.return_value = Mock(spec=RecommendationResultDTO)

        # Act
        result = make_recommendation_service.execute(incomplete_data)

        # Assert
        assert mock_repository.add.called
        # Verify that default values are used
        dto_arg = mock_repository.add.call_args[0][0]
        assert dto_arg.target_sales_amount == 0
        assert "La cantidad óptima a comprar para Test Product y obtener $0 None es 0 unidades." in dto_arg.recommendation

    def test_execute_returns_saved_recommendation(self, make_recommendation_service, sample_sales_data,
                                                  mock_repository):
        """Test that execute returns the saved recommendation from the repository"""
        # Arrange
        make_recommendation_service.calculation_sales_service.calculate_optimum_quantity.return_value = 150

        # Create a specific saved DTO to check the return value
        saved_dto = RecommendationResultDTO(
            id="generated-id-123",
            product_id=sample_sales_data['product']['id'],
            events=json.dumps(sample_sales_data['events']),
            target_sales_amount=sample_sales_data['projection']['salesTarget'],
            currency=sample_sales_data['projection']['currency'],
            recommendation="'La cantidad óptima a comprar para Test Product y obtener $200 USD es 150 unidades.",
            created_at="2023-05-15T10:30:00"
        )
        mock_repository.add.return_value = saved_dto

        # Act
        result = make_recommendation_service.execute(sample_sales_data)

        # Assert
        assert result is saved_dto
        assert result.id == "generated-id-123"
        assert result.created_at == "2023-05-15T10:30:00"
