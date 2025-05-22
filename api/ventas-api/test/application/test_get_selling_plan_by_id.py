import unittest
from unittest.mock import Mock, patch

from src.application.get_selling_plan_by_id import GetSellingPlanById
from src.domain.entities.selling_plan_dto import SellingPlanDTO
from src.application.errors.errors import ResourceNotFoundError


class TestGetSellingPlanById(unittest.TestCase):
    def setUp(self):
        # Create a mock repository
        self.mock_repository = Mock()

        # Create the use case with the mock repository
        self.use_case = GetSellingPlanById(self.mock_repository)

        # Sample data for testing
        self.test_plan_id = "123"
        self.test_selling_plan_data = SellingPlanDTO(
            id=self.test_plan_id,
            user_id="456",
            title="Test Plan",
            description="Test Description",
            target_amount=1000.0,
            target_date="2023-12-31",
            status="active"
        )

    def test_execute_retrieves_selling_plan_successfully(self):
        # Configure mock repository behavior for an existing plan
        self.mock_repository.get_by_id.return_value = self.test_selling_plan_data

        # Execute the use case
        result = self.use_case.execute(self.test_plan_id)

        # Assert repository methods were called with correct parameters
        self.mock_repository.get_by_id.assert_called_once_with(self.test_plan_id)

        # Assert the result is what we expect
        self.assertEqual(result, self.test_selling_plan_data)

    def test_execute_raises_error_for_nonexistent_plan(self):
        # Configure mock repository behavior for a non-existent plan
        self.mock_repository.get_by_id.return_value = None

        # Execute the use case and check for the expected error
        with self.assertRaises(ResourceNotFoundError):
            self.use_case.execute(self.test_plan_id)

        # Assert repository methods were called with correct parameters
        self.mock_repository.get_by_id.assert_called_once_with(self.test_plan_id)

    @patch('src.application.get_selling_plan_by_id.logger')
    def test_logging_is_performed(self, mock_logger):
        # Configure mock repository behavior
        self.mock_repository.get_by_id.return_value = self.test_selling_plan_data

        # Execute the use case
        self.use_case.execute(self.test_plan_id)

        # Verify logging calls were made
        mock_logger.debug.assert_any_call(f"attempting to retrieve selling plan with id: {self.test_plan_id}")
        mock_logger.debug.assert_any_call(f"calling repository method get_by_id for plan id: {self.test_plan_id}")
        mock_logger.debug.assert_any_call(f"successfully retrieved selling plan from repository: {self.test_selling_plan_data.__repr__()}")

    @patch('src.application.get_selling_plan_by_id.logger')
    def test_logging_error_for_nonexistent_plan(self, mock_logger):
        # Configure mock repository behavior for a non-existent plan
        self.mock_repository.get_by_id.return_value = None

        # Execute the use case and catch the expected error
        with self.assertRaises(ResourceNotFoundError):
            self.use_case.execute(self.test_plan_id)

        # Verify error logging was performed
        mock_logger.error.assert_called_once_with(f"selling plan with id {self.test_plan_id} not found in repository")


if __name__ == '__main__':
    unittest.main()