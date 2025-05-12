import unittest
from unittest.mock import Mock, patch
import uuid
from datetime import datetime

from src.application.get_client_visit_record import GetClientVisitRecord
from src.application.errors.errors import RecordNotExistsError
from src.domain.entities.client_visit_record_dto import ClientVisitRecordDTO


class TestGetClientVisitRecord(unittest.TestCase):
    def setUp(self):
        # Create a mock repository
        self.mock_repository = Mock()

        # Create the use case with the mock repository
        self.use_case = GetClientVisitRecord(self.mock_repository)

        # Create sample record ID for testing
        self.sample_record_id = str(uuid.uuid4())

        # Create sample data for testing
        self.sample_visit_data = ClientVisitRecordDTO(
            record_id=self.sample_record_id,
            salesman_id=str(uuid.uuid4()),
            client_id=str(uuid.uuid4()),
            visit_date=datetime.now(),
            notes="Test visit description"
        )

    def test_execute_retrieves_visit_record(self):
        # Arrange
        self.mock_repository.get_visit_record.return_value = self.sample_visit_data

        # Act
        result = self.use_case.execute(self.sample_record_id)

        # Assert
        self.mock_repository.get_visit_record.assert_called_once_with(self.sample_record_id)
        self.assertEqual(result, self.sample_visit_data)

    def test_execute_raises_error_when_record_not_found(self):
        # Arrange
        self.mock_repository.get_visit_record.return_value = None

        # Act and Assert
        with self.assertRaises(RecordNotExistsError):
            self.use_case.execute(self.sample_record_id)

    @patch('src.application.get_client_visit_record.logger')
    def test_execute_logs_debug_messages(self, mock_logger):
        # Arrange
        self.mock_repository.get_visit_record.return_value = self.sample_visit_data

        # Act
        self.use_case.execute(self.sample_record_id)

        # Assert
        mock_logger.debug.assert_any_call(f"Retrieving client visit record: {self.sample_record_id}")
        mock_logger.debug.assert_any_call(
            f"Client visit record retrieved successfully: {self.sample_visit_data.__str__()}")

    @patch('src.application.get_client_visit_record.logger')
    def test_execute_logs_error_when_record_not_found(self, mock_logger):
        # Arrange
        self.mock_repository.get_visit_record.return_value = None

        # Act and Assert
        with self.assertRaises(RecordNotExistsError):
            self.use_case.execute(self.sample_record_id)

        # Verify error was logged
        mock_logger.error.assert_called_once_with(f"Client visit record {self.sample_record_id} not found.")