import pytest
from unittest.mock import Mock, patch

from src.application.get_all_recommendations import GetAllRecommendations
from src.domain.entities.recommentation_result_dto import RecommendationResultDTO


class TestGetAllRecommendations:

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository for testing"""
        return Mock()

    @pytest.fixture
    def get_all_recommendations_service(self, mock_repository):
        """Create an instance of GetAllRecommendations for testing"""
        return GetAllRecommendations(mock_repository)

    @pytest.fixture
    def sample_recommendations(self):
        """Create sample recommendation DTOs for testing"""
        return [
            RecommendationResultDTO(
                id="1",
                product_id="PROD-123",
                events={"event1": "data1"},
                target_sales_amount=1500.0,
                currency="USD",
                recommendation="Buy 100 units",
                created_at="2023-05-15T10:30:00"
            ),
            RecommendationResultDTO(
                id="2",
                product_id="PROD-456",
                events={"event2": "data2"},
                target_sales_amount=2000.0,
                currency="EUR",
                recommendation="Buy 150 units",
                created_at="2023-05-16T11:30:00"
            )
        ]

    def test_execute_returns_recommendations(self, get_all_recommendations_service, mock_repository, sample_recommendations):
        """Test execute method returns recommendations from repository"""
        # Arrange
        mock_repository.get_all.return_value = sample_recommendations

        # Act
        result = get_all_recommendations_service.execute()

        # Assert
        assert result == sample_recommendations
        mock_repository.get_all.assert_called_once()

    def test_execute_returns_empty_list(self, get_all_recommendations_service, mock_repository):
        """Test execute method returns empty list when no recommendations exist"""
        # Arrange
        mock_repository.get_all.return_value = []

        # Act
        result = get_all_recommendations_service.execute()

        # Assert
        assert result == []
        assert len(result) == 0
        mock_repository.get_all.assert_called_once()

    @patch('src.application.get_all_recommendations.logger')
    def test_execute_logs_correctly(self, mock_logger, get_all_recommendations_service,
                                   mock_repository, sample_recommendations):
        """Test that the execute method logs correctly"""
        # Arrange
        mock_repository.get_all.return_value = sample_recommendations

        # Act
        get_all_recommendations_service.execute()

        # Assert
        mock_logger.debug.assert_called_with("Starting the retrieval of all recommendations")
        mock_logger.info.assert_called_with("Retrieval of all recommendations completed successfully")

    def test_execute_repository_called(self, get_all_recommendations_service, mock_repository):
        """Test that the repository's get_all method is called"""
        # Act
        get_all_recommendations_service.execute()

        # Assert
        mock_repository.get_all.assert_called_once()