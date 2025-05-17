import unittest
from unittest.mock import Mock, patch
from src.application.get_clients_by_salesman import GetClientsBySalesman
from src.domain.entities.client_salesman_dto import ClientSalesmanDTO


class TestGetClientsBySalesman(unittest.TestCase):
    def setUp(self):
        # Create a mock repository
        self.mock_repository = Mock()

        # Create the use case with the mock repository
        self.use_case = GetClientsBySalesman(self.mock_repository)

        # Sample data for testing
        self.test_salesman_id = "456"
        self.sample_clients = [
            ClientSalesmanDTO(
                id="123",
                salesman_id=self.test_salesman_id,
                client_id="789",
                client_name="Test Client 1",
                client_phone="123456789",
                client_email="client1@example.com",
                address="Test Address 1",
                city="Test City 1",
                country="Test Country 1",
                store_name="Test Store 1"
            ),
            ClientSalesmanDTO(
                id="124",
                salesman_id=self.test_salesman_id,
                client_id="790",
                client_name="Test Client 2",
                client_phone="987654321",
                client_email="client2@example.com",
                address="Test Address 2",
                city="Test City 2",
                country="Test Country 2",
                store_name="Test Store 2"
            )
        ]

    def test_execute_returns_clients_from_repository(self):
        # Configure the mock repository to return sample clients
        self.mock_repository.get_clients_salesman.return_value = self.sample_clients

        # Execute the use case
        result = self.use_case.execute(self.test_salesman_id)

        # Assert the repository method was called with correct parameters
        self.mock_repository.get_clients_salesman.assert_called_once_with(self.test_salesman_id)

        # Assert the result is what we expect
        self.assertEqual(result, self.sample_clients)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].client_name, "Test Client 1")
        self.assertEqual(result[1].client_name, "Test Client 2")

    def test_execute_returns_empty_list_when_no_clients(self):
        # Configure the mock repository to return an empty list
        self.mock_repository.get_clients_salesman.return_value = []

        # Execute the use case
        result = self.use_case.execute(self.test_salesman_id)

        # Assert the repository method was called with correct parameters
        self.mock_repository.get_clients_salesman.assert_called_once_with(self.test_salesman_id)

        # Assert the result is an empty list
        self.assertEqual(result, [])
        self.assertEqual(len(result), 0)

    @patch('src.application.get_clients_by_salesman.logger')
    def test_logging_is_performed(self, mock_logger):
        # Configure the mock repository
        self.mock_repository.get_clients_salesman.return_value = self.sample_clients

        # Execute the use case
        self.use_case.execute(self.test_salesman_id)

        # Verify logging calls were made
        mock_logger.debug.assert_any_call(f"Getting clients for salesman ID: {self.test_salesman_id}")
        mock_logger.debug.assert_any_call(f"Clients retrieved: {self.sample_clients}")


if __name__ == '__main__':
    unittest.main()