import unittest
from datetime import datetime

from src.domain.entities.reports.order_reports_dto import OrderReportsDTO
from src.infrastructure.mapper.order_reports_mapper import OrderReportsMapper
from src.infrastructure.model.order_reports_model import OrderReportsModel


class TestOrderReportsMapper(unittest.TestCase):

    def setUp(self):
        # Setup test data
        self.report_id = "report123"
        self.user_id = "user456"
        self.report_name = "Sales Report"
        self.report_date = datetime(2023, 5, 15, 10, 30, 0)
        self.url = "https://example.com/reports/report123.pdf"

        # Create model and DTO instances for testing
        self.model = OrderReportsModel(
            id=self.report_id,
            user_id=self.user_id,
            name=self.report_name,
            date=self.report_date,
            url=self.url
        )

        self.dto = OrderReportsDTO(
            report_id=self.report_id,
            user_id=self.user_id,
            report_name=self.report_name,
            report_date=self.report_date,
            url=self.url
        )

        self.dto_with_string_date = OrderReportsDTO(
            report_id=self.report_id,
            user_id=self.user_id,
            report_name=self.report_name,
            report_date=self.report_date.isoformat(),
            url=self.url
        )

    def test_to_dto(self):
        # Test conversion from model to DTO
        result = OrderReportsMapper.to_dto(self.model)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, OrderReportsDTO)
        self.assertEqual(result.report_id, self.report_id)
        self.assertEqual(result.user_id, self.user_id)
        self.assertEqual(result.report_name, self.report_name)
        self.assertEqual(result.report_date, self.report_date.isoformat())
        self.assertEqual(result.url, self.url)

    def test_to_dto_with_none(self):
        # Test conversion with None model
        result = OrderReportsMapper.to_dto(None)
        self.assertIsNone(result)

    def test_to_model(self):
        # Test conversion from DTO to model
        result = OrderReportsMapper.to_model(self.dto)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, OrderReportsModel)
        self.assertEqual(result.id, self.report_id)
        self.assertEqual(result.user_id, self.user_id)
        self.assertEqual(result.name, self.report_name)
        self.assertEqual(result.date, self.report_date)
        self.assertEqual(result.url, self.url)

    def test_to_model_with_string_date(self):
        # Test conversion from DTO with string date to model
        result = OrderReportsMapper.to_model(self.dto_with_string_date)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, OrderReportsModel)
        self.assertEqual(result.id, self.report_id)
        self.assertEqual(result.date, self.report_date)

    def test_to_model_with_none(self):
        # Test conversion with None DTO
        result = OrderReportsMapper.to_model(None)
        self.assertIsNone(result)

    def test_to_dto_list(self):
        # Test conversion from list of models to list of DTOs
        models = [self.model, self.model]
        result = OrderReportsMapper.to_dto_list(models)

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], OrderReportsDTO)
        self.assertEqual(result[0].report_id, self.report_id)

    def test_to_model_list(self):
        # Test conversion from list of DTOs to list of models
        dtos = [self.dto, self.dto]
        result = OrderReportsMapper.to_model_list(dtos)

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], OrderReportsModel)
        self.assertEqual(result[0].id, self.report_id)


if __name__ == '__main__':
    unittest.main()
