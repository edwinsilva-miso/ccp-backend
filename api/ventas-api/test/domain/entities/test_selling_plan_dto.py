import unittest
from src.domain.entities.selling_plan_dto import SellingPlanDTO


class TestSellingPlanDTO(unittest.TestCase):
    def setUp(self):
        # Setup test data
        self.test_id = "123"
        self.test_user_id = "456"
        self.test_title = "Test Plan"
        self.test_description = "Test Description"
        self.test_target_amount = 1000.0
        self.test_target_date = "2023-12-31"
        self.test_status = "active"
        self.test_created_at = "2023-01-01T12:00:00"

        # Create sample DTO for testing
        self.sample_dto = SellingPlanDTO(
            id=self.test_id,
            user_id=self.test_user_id,
            title=self.test_title,
            description=self.test_description,
            target_amount=self.test_target_amount,
            target_date=self.test_target_date,
            status=self.test_status,
            created_at=self.test_created_at
        )

    def test_initialization(self):
        # Test that the DTO is initialized with the correct values
        self.assertEqual(self.sample_dto.id, self.test_id)
        self.assertEqual(self.sample_dto.user_id, self.test_user_id)
        self.assertEqual(self.sample_dto.title, self.test_title)
        self.assertEqual(self.sample_dto.description, self.test_description)
        self.assertEqual(self.sample_dto.target_amount, self.test_target_amount)
        self.assertEqual(self.sample_dto.target_date, self.test_target_date)
        self.assertEqual(self.sample_dto.status, self.test_status)
        self.assertEqual(self.sample_dto.created_at, self.test_created_at)

    def test_to_dict(self):
        # Test conversion to dictionary
        result = self.sample_dto.to_dict()
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], self.test_id)
        self.assertEqual(result["user_id"], self.test_user_id)
        self.assertEqual(result["title"], self.test_title)
        self.assertEqual(result["description"], self.test_description)
        self.assertEqual(result["target_amount"], self.test_target_amount)
        self.assertEqual(result["target_date"], self.test_target_date)
        self.assertEqual(result["status"], self.test_status)
        self.assertEqual(result["created_at"], self.test_created_at)

    def test_default_values(self):
        # Test that default values are set correctly
        dto = SellingPlanDTO(
            id="test",
            user_id="test_user",
            title="Test Title",
            description="Test Description"
        )
        
        self.assertEqual(dto.status, "active")
        self.assertIsNone(dto.target_amount)
        self.assertIsNone(dto.target_date)
        self.assertIsNone(dto.created_at)


if __name__ == '__main__':
    unittest.main()