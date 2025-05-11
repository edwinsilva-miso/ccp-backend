import unittest
from unittest.mock import Mock, patch

from src.application.get_selling_plans_by_user_id import GetSellingPlansByUserId
from src.domain.entities.selling_plan_dto import SellingPlanDTO


class TestGetSellingPlansByUserId(unittest.TestCase):
    def setUp(self):
        # Create a mock repository
        self.mock_repository = Mock()

        # Create the use case with the mock repository
        self.use_case = GetSellingPlansByUserId(self.mock_repository)

        # Sample data for testing
        self.test_user_id = "456"
        self.test_selling_plans = [
            SellingPlanDTO(
                id="123",
                user_id=self.test_user_id,
                title="Test Plan 1",
                description="Test Description 1",
                target_amount=1000.0,
                target_date="2023-12-31",
                status="active"
            ),
            SellingPlanDTO(
                id="456",
                user_id=self.test_user_id,
                title="Test Plan 2",
                description="Test Description 2",
                target_amount=2000.0,
                target_date="2024-06-30",
                status="completed"
            )
        ]

    def test_execute_retrieves_selling_plans_successfully(self):
        # Configure mock repository behavior
        self.mock_repository.get_by_user_id.return_value = self.test_selling_plans

        # Execute the use case
        result = self.use_case.execute(self.test_user_id)

        # Assert repository methods were called with correct parameters
        self.mock_repository.get_by_user_id.assert_called_once_with(self.test_user_id)

        # Assert the result is what we expect
        self.assertEqual(result, self.test_selling_plans)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "123")
        self.assertEqual(result[1].id, "456")

    def test_execute_returns_empty_list_when_no_plans_found(self):
        # Configure mock repository behavior for no plans
        self.mock_repository.get_by_user_id.return_value = []

        # Execute the use case
        result = self.use_case.execute(self.test_user_id)

        # Assert repository methods were called with correct parameters
        self.mock_repository.get_by_user_id.assert_called_once_with(self.test_user_id)

        # Assert the result is an empty list
        self.assertEqual(result, [])
        self.assertEqual(len(result), 0)

    @patch('src.application.get_selling_plans_by_user_id.logger')
    def test_logging_is_performed(self, mock_logger):
        # Configure mock repository behavior
        self.mock_repository.get_by_user_id.return_value = self.test_selling_plans

        # Execute the use case
        self.use_case.execute(self.test_user_id)

        # Verify logging calls were made
        mock_logger.debug.assert_any_call(f"Retrieving selling plans for user with ID: {self.test_user_id}")
        mock_logger.debug.assert_any_call(f"Retrieved {len(self.test_selling_plans)} selling plans for user with ID: {self.test_user_id}")


if __name__ == '__main__':
    unittest.main()