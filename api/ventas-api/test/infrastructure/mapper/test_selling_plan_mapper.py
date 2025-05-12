import unittest
from datetime import datetime
from unittest.mock import patch

from src.infrastructure.mapper.selling_plan_mapper import SellingPlanMapper
from src.infrastructure.model.selling_plan_model import SellingPlanModel
from src.domain.entities.selling_plan_dto import SellingPlanDTO


class TestSellingPlanMapper(unittest.TestCase):
    def setUp(self):
        # Setup test data
        self.test_id = "123"
        self.test_user_id = "456"
        self.test_title = "Test Plan"
        self.test_description = "Test Description"
        self.test_target_amount = 1000.0
        self.test_target_date = "2023-12-31"
        self.test_status = "active"
        self.test_created_at = datetime.utcnow()

        # Create sample model and DTO for testing
        self.sample_model = SellingPlanModel(
            id=self.test_id,
            user_id=self.test_user_id,
            title=self.test_title,
            description=self.test_description,
            target_amount=self.test_target_amount,
            target_date=self.test_target_date,
            status=self.test_status,
            created_at=self.test_created_at
        )

        self.sample_dto = SellingPlanDTO(
            id=self.test_id,
            user_id=self.test_user_id,
            title=self.test_title,
            description=self.test_description,
            target_amount=self.test_target_amount,
            target_date=self.test_target_date,
            status=self.test_status,
            created_at=self.test_created_at.isoformat() if self.test_created_at else None
        )

    @patch('src.infrastructure.mapper.selling_plan_mapper.logger')
    def test_to_dto(self, mock_logger):
        # Test conversion from model to DTO
        result = SellingPlanMapper.to_dto(self.sample_model)

        self.assertIsInstance(result, SellingPlanDTO)
        self.assertEqual(result.id, self.test_id)
        self.assertEqual(result.user_id, self.test_user_id)
        self.assertEqual(result.title, self.test_title)
        self.assertEqual(result.description, self.test_description)
        self.assertEqual(result.target_amount, self.test_target_amount)
        self.assertEqual(result.target_date, self.test_target_date)
        self.assertEqual(result.status, self.test_status)
        self.assertEqual(result.created_at, self.test_created_at.isoformat())

        # Verify logging
        mock_logger.debug.assert_any_call(f"converting selling plan model to dto: {self.sample_model.__dict__}")
        mock_logger.debug.assert_any_call(f"successfully converted to dto: {result.__dict__}")

    @patch('src.infrastructure.mapper.selling_plan_mapper.logger')
    def test_to_model(self, mock_logger):
        # Test conversion from DTO to model
        result = SellingPlanMapper.to_model(self.sample_dto)

        self.assertIsInstance(result, SellingPlanModel)
        self.assertEqual(result.id, self.test_id)
        self.assertEqual(result.user_id, self.test_user_id)
        self.assertEqual(result.title, self.test_title)
        self.assertEqual(result.description, self.test_description)
        self.assertEqual(result.target_amount, self.test_target_amount)
        self.assertEqual(result.target_date, self.test_target_date)
        self.assertEqual(result.status, self.test_status)

        # Verify logging
        mock_logger.debug.assert_any_call(f"converting selling plan dto to model: {self.sample_dto.__dict__}")
        mock_logger.debug.assert_any_call(f"successfully converted to model: {result.__dict__}")

    @patch('src.infrastructure.mapper.selling_plan_mapper.logger')
    def test_to_dto_list(self, mock_logger):
        # Test conversion from list of models to list of DTOs
        models = [self.sample_model, self.sample_model]
        result = SellingPlanMapper.to_dto_list(models)

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], SellingPlanDTO)
        self.assertIsInstance(result[1], SellingPlanDTO)
        self.assertEqual(result[0].id, self.test_id)
        self.assertEqual(result[1].id, self.test_id)

        # Verify logging
        mock_logger.debug.assert_any_call(f"converting list of {len(models)} selling plan models to dtos")
        mock_logger.debug.assert_any_call(f"successfully converted {len(result)} models to dtos")

    @patch('src.infrastructure.mapper.selling_plan_mapper.logger')
    def test_to_model_list(self, mock_logger):
        # Test conversion from list of DTOs to list of models
        dtos = [self.sample_dto, self.sample_dto]
        result = SellingPlanMapper.to_model_list(dtos)

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], SellingPlanModel)
        self.assertIsInstance(result[1], SellingPlanModel)
        self.assertEqual(result[0].id, self.test_id)
        self.assertEqual(result[1].id, self.test_id)

        # Verify logging
        mock_logger.debug.assert_any_call(f"converting list of {len(dtos)} selling plan dtos to models")
        mock_logger.debug.assert_any_call(f"successfully converted {len(result)} dtos to models")

    def test_empty_list_conversions(self):
        # Test handling of empty lists
        self.assertEqual(SellingPlanMapper.to_dto_list([]), [])
        self.assertEqual(SellingPlanMapper.to_model_list([]), [])


if __name__ == '__main__':
    unittest.main()