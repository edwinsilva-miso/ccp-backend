import unittest
from unittest.mock import Mock, patch
import uuid
from datetime import datetime

from src.application.get_visits_by_salesman import GetVisitsBySalesman
from src.domain.entities.client_visit_record_dto import ClientVisitRecordDTO


class TestGetVisitsBySalesman(unittest.TestCase):
    def setUp(self):
        # Create a mock repository
        self.mock_repository = Mock()

        # Create the use case with the mock repository
        self.use_case = GetVisitsBySalesman(self.mock_repository)

        # Create sample salesman ID for testing
        self.sample_salesman_id = str(uuid.uuid4())

        # Create sample data for testing
        self.sample_visits = [
            ClientVisitRecordDTO(
                record_id=str(uuid.uuid4()),
                salesman_id=self.sample_salesman_id,
                client_id=str(uuid.uuid4()),
                visit_date=datetime.now(),
                notes="Visit 1 description"
            ),
            ClientVisitRecordDTO(
                record_id=str(uuid.uuid4()),
                salesman_id=self.sample_salesman_id,
                client_id=str(uuid.uuid4()),
                visit_date=datetime.now(),
                notes="Visit 2 description"
            )
        ]

    def test_execute_retrieves_visits_by_salesman(self):
        # Arrange
        self.mock_repository.get_visit_records_by_salesman.return_value = self.sample_visits

        # Act
        result = self.use_case.execute(self.sample_salesman_id)

        # Assert
        self.mock_repository.get_visit_records_by_salesman.assert_called_once_with(self.sample_salesman_id)
        self.assertEqual(result, self.sample_visits)
        self.assertEqual(len(result), 2)

    def test_execute_returns_empty_list_when_no_visits_found(self):
        # Arrange
        self.mock_repository.get_visit_records_by_salesman.return_value = []

        # Act
        result = self.use_case.execute(self.sample_salesman_id)

        # Assert
        self.assertEqual(result, [])
        self.assertEqual(len(result), 0)

    @patch('src.application.get_visits_by_salesman.logger')
    def test_execute_logs_debug_messages(self, mock_logger):
        # Arrange
        self.mock_repository.get_visit_records_by_salesman.return_value = self.sample_visits

        # Act
        self.use_case.execute(self.sample_salesman_id)

        # Assert
        mock_logger.debug.assert_any_call(f"Retrieving visits for salesman: {self.sample_salesman_id}")
        mock_logger.debug.assert_any_call(f"Visits retrieved successfully: {self.sample_visits}")