import unittest
from unittest.mock import Mock, patch
from src.application.associate_client import AssociateClient
from src.domain.entities.client_salesman_dto import ClientSalesmanDTO
from src.application.errors.errors import ClientAlreadyAssociatedError


class TestAssociateClient(unittest.TestCase):
    def setUp(self):
        # Create a mock repository
        self.mock_repository = Mock()

        # Create the use case with the mock repository
        self.use_case = AssociateClient(self.mock_repository)

        # Sample data for testing
        self.test_client_data = ClientSalesmanDTO(
            id="123",
            salesman_id="456",
            client_id="789",
            client_name="Test Client",
            client_phone="123456789",
            client_email="test@example.com",
            address="Test Address",
            city="Test City",
            country="Test Country",
            store_name="Test Store"
        )

    def test_execute_associates_new_client_successfully(self):
        # Configure mock repository behavior for a new client
        self.mock_repository.get_client_by_id.return_value = None
        self.mock_repository.add.return_value = self.test_client_data

        # Execute the use case
        result = self.use_case.execute(self.test_client_data)

        # Assert repository methods were called with correct parameters
        self.mock_repository.get_client_by_id.assert_called_once_with(self.test_client_data.client_id)
        self.mock_repository.add.assert_called_once_with(self.test_client_data)

        # Assert the result is what we expect
        self.assertEqual(result, self.test_client_data)

    def test_execute_raises_error_for_already_associated_client(self):
        # Configure mock repository behavior for an existing client
        self.mock_repository.get_client_by_id.return_value = self.test_client_data

        # Execute the use case and check for the expected error
        with self.assertRaises(ClientAlreadyAssociatedError):
            self.use_case.execute(self.test_client_data)

        # Assert repository methods were called with correct parameters
        self.mock_repository.get_client_by_id.assert_called_once_with(self.test_client_data.client_id)
        self.mock_repository.add.assert_not_called()

    @patch('src.application.associate_client.logger')
    def test_logging_is_performed(self, mock_logger):
        # Configure mock repository behavior
        self.mock_repository.get_client_by_id.return_value = None
        self.mock_repository.add.return_value = self.test_client_data

        # Execute the use case
        self.use_case.execute(self.test_client_data)

        # Verify logging calls were made
        mock_logger.debug.assert_any_call(f"Associating client: {self.test_client_data.__str__()}")
        mock_logger.debug.assert_any_call(f"Client associated successfully: {self.test_client_data.__str__()}")

    @patch('src.application.associate_client.logger')
    def test_logging_error_for_existing_client(self, mock_logger):
        # Configure mock repository behavior for an existing client
        self.mock_repository.get_client_by_id.return_value = self.test_client_data

        # Execute the use case and catch the expected error
        with self.assertRaises(ClientAlreadyAssociatedError):
            self.use_case.execute(self.test_client_data)

        # Verify error logging was performed
        mock_logger.error.assert_called_once_with(f"Client {self.test_client_data.client_id} already associated.")


if __name__ == '__main__':
    unittest.main()