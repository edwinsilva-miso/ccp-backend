import pytest
import datetime
from unittest.mock import patch, MagicMock
from datetime import timedelta

# Fix the import paths to match your project structure
from src.domain.service.calculation_sales_service import CalculationSalesService
from src.domain.exceptions.recommendation_error import RecommendationError


class TestCalculationSalesService:

    @pytest.fixture
    def service(self):
        """Create an instance of CalculationSalesService for testing"""
        return CalculationSalesService()

    @pytest.fixture
    def sample_sales_data(self):
        """Create sample sales data for testing"""
        return {
            'product': {
                'id': 'PROD-123',
                'stock': 50
            },
            'projection': {
                'salesTarget': 200
            },
            'events': []
        }

    def test_calculate_optimum_quantity_basic(self, service, sample_sales_data):
        """Test basic calculation with no events"""
        # Act
        result = service.calculate_optimum_quantity(sample_sales_data)

        # Assert
        assert result == 150  # 200 (target) - 50 (stock)

    def test_calculate_optimum_quantity_zero_stock(self, service, sample_sales_data):
        """Test calculation when current stock is zero"""
        # Arrange
        sample_sales_data['product']['stock'] = 0

        # Act
        result = service.calculate_optimum_quantity(sample_sales_data)

        # Assert
        assert result == 200  # 200 (target) - 0 (stock)

    def test_calculate_optimum_quantity_high_stock(self, service, sample_sales_data):
        """Test calculation when current stock exceeds target"""
        # Arrange
        sample_sales_data['product']['stock'] = 250

        # Act
        result = service.calculate_optimum_quantity(sample_sales_data)

        # Assert
        assert result == 0  # No need to order more

    @patch('src.domain.service.calculation_sales_service.datetime')
    def test_calculate_optimum_quantity_near_event(self, mock_datetime, service, sample_sales_data):
        """Test calculation with a near future event"""
        # Arrange
        today = datetime.date(2023, 5, 15)
        mock_datetime.date.today.return_value = today

        # Create a mock date 15 days in the future
        event_date_str = (today + timedelta(days=15)).strftime('%Y-%m-%d')
        mock_event_date = today + timedelta(days=15)

        # Set up the mock strptime to return our mocked date
        mock_datetime.datetime.strptime.return_value = datetime.datetime.combine(
            mock_event_date, datetime.datetime.min.time()
        )

        sample_sales_data['events'] = [{'date': event_date_str, 'name': 'Sale Event'}]

        # Act
        result = service.calculate_optimum_quantity(sample_sales_data)

        # Assert
        expected = max(0, int(200 * 1.1) - 50)  # (200 * 1.1) - 50
        assert result == expected

    @patch('src.domain.service.calculation_sales_service.datetime')
    def test_calculate_optimum_quantity_medium_event(self, mock_datetime, service, sample_sales_data):
        """Test calculation with a medium future event"""
        # Arrange
        today = datetime.date(2023, 5, 15)
        mock_datetime.date.today.return_value = today

        event_date_str = (today + timedelta(days=60)).strftime('%Y-%m-%d')
        mock_event_date = today + timedelta(days=60)

        mock_datetime.datetime.strptime.return_value = datetime.datetime.combine(
            mock_event_date, datetime.datetime.min.time()
        )

        sample_sales_data['events'] = [{'date': event_date_str, 'name': 'Sale Event'}]

        # Act
        result = service.calculate_optimum_quantity(sample_sales_data)

        # Assert
        expected = max(0, int(200 * 1.05) - 50)  # (200 * 1.05) - 50
        assert result == expected

    @patch('src.domain.service.calculation_sales_service.datetime')
    def test_calculate_optimum_quantity_far_event(self, mock_datetime, service, sample_sales_data):
        """Test calculation with a far future event"""
        # Arrange
        today = datetime.date(2023, 5, 15)
        mock_datetime.date.today.return_value = today

        event_date_str = (today + timedelta(days=150)).strftime('%Y-%m-%d')
        mock_event_date = today + timedelta(days=150)

        mock_datetime.datetime.strptime.return_value = datetime.datetime.combine(
            mock_event_date, datetime.datetime.min.time()
        )

        sample_sales_data['events'] = [{'date': event_date_str, 'name': 'Sale Event'}]

        # Act
        result = service.calculate_optimum_quantity(sample_sales_data)

        # Assert
        expected = max(0, int(200 * 0.9) - 50)  # (200 * 0.9) - 50
        assert result == expected

    @patch('src.domain.service.calculation_sales_service.datetime')
    def test_calculate_optimum_quantity_multiple_events(self, mock_datetime, service, sample_sales_data):
        """Test calculation with multiple events"""
        # Arrange
        today = datetime.date(2023, 5, 15)
        mock_datetime.date.today.return_value = today

        near_date_str = (today + timedelta(days=15)).strftime('%Y-%m-%d')
        medium_date_str = (today + timedelta(days=60)).strftime('%Y-%m-%d')
        far_date_str = (today + timedelta(days=150)).strftime('%Y-%m-%d')

        # Setup a side_effect for strptime to return different dates for different inputs
        def strptime_side_effect(date_str, _):
            if date_str == near_date_str:
                return datetime.datetime.combine(today + timedelta(days=15), datetime.datetime.min.time())
            elif date_str == medium_date_str:
                return datetime.datetime.combine(today + timedelta(days=60), datetime.datetime.min.time())
            elif date_str == far_date_str:
                return datetime.datetime.combine(today + timedelta(days=150), datetime.datetime.min.time())
            return None

        mock_datetime.datetime.strptime.side_effect = strptime_side_effect

        sample_sales_data['events'] = [
            {'date': near_date_str, 'name': 'Near Event'},
            {'date': medium_date_str, 'name': 'Medium Event'},
            {'date': far_date_str, 'name': 'Far Event'}
        ]

        # Act
        result = service.calculate_optimum_quantity(sample_sales_data)

        # Assert
        # 1.1 * 1.05 * 0.9 = 1.0395
        expected = max(0, int(200 * 1.1 * 1.05 * 0.9) - 50)
        assert result == expected

    def test_calculate_optimum_quantity_missing_data(self, service):
        """Test calculation with missing data"""
        # Arrange
        incomplete_data = {
            'product': {},
            'projection': {}
        }

        # Act
        result = service.calculate_optimum_quantity(incomplete_data)

        # Assert
        assert result == 0  # Default values should be used

    def test_calculate_optimum_quantity_exception(self, service):
        """Test calculation with invalid data causing exception"""
        # Arrange
        invalid_data = None

        # Act & Assert
        with pytest.raises(RecommendationError):
            service.calculate_optimum_quantity(invalid_data)