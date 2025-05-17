import unittest
from unittest.mock import Mock, patch
import uuid
from datetime import datetime

from src.application.add_client_visit import AddClientVisit
from src.domain.entities.client_visit_record_dto import ClientVisitRecordDTO


class TestAddClientVisit(unittest.TestCase):
    def setUp(self):
        # Create a mock repository
        self.mock_repository = Mock()

        # Create the use case with the mock repository
        self.use_case = AddClientVisit(self.mock_repository)

        # Create sample data for testing
        self.sample_visit_data = ClientVisitRecordDTO(
            record_id=str(uuid.uuid4()),
            salesman_id=str(uuid.uuid4()),
            client_id=str(uuid.uuid4()),
            visit_date=datetime.now(),
            notes="Test visit description",
        )

        # Configure mock to return a specific value when add_visit_record is called
        self.mock_repository.add_visit_record.return_value = self.sample_visit_data

    def test_execute_adds_visit_record(self):
        # Act
        result = self.use_case.execute(self.sample_visit_data)

        # Assert
        self.mock_repository.add_visit_record.assert_called_once_with(self.sample_visit_data)
        self.assertEqual(result, self.sample_visit_data)

    @patch('src.application.add_client_visit.logger')
    def test_execute_logs_debug_messages(self, mock_logger):
        # Act
        self.use_case.execute(self.sample_visit_data)

        # Assert
        mock_logger.debug.assert_any_call(f"Adding client visit record: {self.sample_visit_data.__str__()}")
        mock_logger.debug.assert_any_call(f"Client visit record added successfully: {self.sample_visit_data.__str__()}")

    def test_execute_returns_repository_response(self):
        # Arrange
        custom_response = ClientVisitRecordDTO(
            record_id="custom-id",
            salesman_id=str(uuid.uuid4()),
            client_id=str(uuid.uuid4()),
            visit_date=datetime.now(),
            notes="Custom description"
        )
        self.mock_repository.add_visit_record.return_value = custom_response

        # Act
        result = self.use_case.execute(self.sample_visit_data)

        # Assert
        self.assertEqual(result, custom_response)