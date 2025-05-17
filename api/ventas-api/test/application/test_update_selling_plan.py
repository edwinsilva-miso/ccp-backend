import unittest
from unittest.mock import Mock, patch

from src.application.update_selling_plan import UpdateSellingPlan
from src.domain.entities.selling_plan_dto import SellingPlanDTO
from src.application.errors.errors import ResourceNotFoundError


class TestUpdateSellingPlan(unittest.TestCase):
    def setUp(self):
        # Create a mock repository
        self.mock_repository = Mock()

        # Create the use case with the mock repository
        self.use_case = UpdateSellingPlan(self.mock_repository)

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

    def test_execute_updates_selling_plan_successfully(self):
        # Configure mock repository behavior for an existing plan
        self.mock_repository.get_by_id.return_value = self.test_selling_plan_data
        self.mock_repository.update.return_value = self.test_selling_plan_data

        # Execute the use case
        result = self.use_case.execute(self.test_selling_plan_data)

        # Assert repository methods were called with correct parameters
        self.mock_repository.get_by_id.assert_called_once_with(self.test_selling_plan_data.id)
        self.mock_repository.update.assert_called_once_with(self.test_selling_plan_data)

        # Assert the result is what we expect
        self.assertEqual(result, self.test_selling_plan_data)

    def test_execute_raises_error_for_nonexistent_plan(self):
        # Configure mock repository behavior for a non-existent plan
        self.mock_repository.get_by_id.return_value = None

        # Execute the use case and check for the expected error
        with self.assertRaises(ResourceNotFoundError):
            self.use_case.execute(self.test_selling_plan_data)

        # Assert repository methods were called with correct parameters
        self.mock_repository.get_by_id.assert_called_once_with(self.test_selling_plan_data.id)
        self.mock_repository.update.assert_not_called()

    @patch('src.application.update_selling_plan.logger')
    def test_logging_is_performed(self, mock_logger):
        # Configure mock repository behavior
        self.mock_repository.get_by_id.return_value = self.test_selling_plan_data
        self.mock_repository.update.return_value = self.test_selling_plan_data

        # Execute the use case
        self.use_case.execute(self.test_selling_plan_data)

        # Verify logging calls were made
        mock_logger.debug.assert_any_call(f"Updating selling plan: {self.test_selling_plan_data.__repr__()}")
        mock_logger.debug.assert_any_call(f"Selling plan updated successfully: {self.test_selling_plan_data.__repr__()}")

    @patch('src.application.update_selling_plan.logger')
    def test_logging_error_for_nonexistent_plan(self, mock_logger):
        # Configure mock repository behavior for a non-existent plan
        self.mock_repository.get_by_id.return_value = None

        # Execute the use case and catch the expected error
        with self.assertRaises(ResourceNotFoundError):
            self.use_case.execute(self.test_selling_plan_data)

        # Verify error logging was performed
        mock_logger.error.assert_called_once_with(f"Selling plan with ID {self.test_selling_plan_data.id} not found.")


if __name__ == '__main__':
    unittest.main()