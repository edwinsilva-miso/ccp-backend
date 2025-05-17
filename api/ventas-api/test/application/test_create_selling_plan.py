import unittest
from unittest.mock import Mock, patch

from src.application.create_selling_plan import CreateSellingPlan
from src.domain.entities.selling_plan_dto import SellingPlanDTO


class TestCreateSellingPlan(unittest.TestCase):
    def setUp(self):
        # Create a mock repository
        self.mock_repository = Mock()

        # Create the use case with the mock repository
        self.use_case = CreateSellingPlan(self.mock_repository)

        # Sample data for testing
        self.test_selling_plan_data = SellingPlanDTO(
            id="123",
            user_id="456",
            title="Test Plan",
            description="Test Description",
            target_amount=1000.0,
            target_date="2023-12-31",
            status="active"
        )

    def test_execute_creates_selling_plan_successfully(self):
        # Configure mock repository behavior
        self.mock_repository.add.return_value = self.test_selling_plan_data

        # Execute the use case
        result = self.use_case.execute(self.test_selling_plan_data)

        # Assert repository methods were called with correct parameters
        self.mock_repository.add.assert_called_once_with(self.test_selling_plan_data)

        # Assert the result is what we expect
        self.assertEqual(result, self.test_selling_plan_data)

    @patch('src.application.create_selling_plan.logger')
    def test_logging_is_performed(self, mock_logger):
        # Configure mock repository behavior
        self.mock_repository.add.return_value = self.test_selling_plan_data

        # Execute the use case
        self.use_case.execute(self.test_selling_plan_data)

        # Verify logging calls were made
        mock_logger.debug.assert_any_call(f"starting creation of new selling plan with data: {self.test_selling_plan_data.__repr__()}")
        mock_logger.debug.assert_any_call("validating selling plan data before creation")
        mock_logger.debug.assert_any_call("attempting to add new selling plan to repository")
        mock_logger.debug.assert_any_call(f"selling plan successfully created and stored: {self.test_selling_plan_data.__repr__()}")


if __name__ == '__main__':
    unittest.main()