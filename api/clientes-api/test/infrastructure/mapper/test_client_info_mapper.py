import unittest
from unittest.mock import Mock

from src.domain.entities.client_info_dto import ClientInfoDTO
from src.infrastructure.mapper.client_info_mapper import ClientInfoMapper
from src.infrastructure.model.client_info_model import ClientInfoModel


class TestClientInfoMapper(unittest.TestCase):
    def setUp(self):
        # Create sample model
        self.mock_client_info_model = Mock(spec=ClientInfoModel)
        self.mock_client_info_model.name = "John Doe"
        self.mock_client_info_model.address = "123 Main St"
        self.mock_client_info_model.phone = "555-1234"
        self.mock_client_info_model.email = "john.doe@example.com"
        self.mock_client_info_model.order_id = "order123"

        # Create sample DTO
        self.mock_client_info_dto = ClientInfoDTO(
            name="John Doe",
            address="123 Main St",
            phone="555-1234",
            email="john.doe@example.com",
            order_id="order123"
        )

    def test_to_dto(self):
        # Execute
        result = ClientInfoMapper.to_dto(self.mock_client_info_model)

        # Verify
        self.assertEqual(result.name, self.mock_client_info_model.name)
        self.assertEqual(result.address, self.mock_client_info_model.address)
        self.assertEqual(result.phone, self.mock_client_info_model.phone)
        self.assertEqual(result.email, self.mock_client_info_model.email)
        self.assertEqual(result.order_id, self.mock_client_info_model.order_id)

    def test_to_dto_none(self):
        # Execute
        result = ClientInfoMapper.to_dto(None)

        # Verify
        self.assertIsNone(result)

    def test_to_model(self):
        # Execute
        result = ClientInfoMapper.to_model(self.mock_client_info_dto)

        # Verify
        self.assertEqual(result.name, self.mock_client_info_dto.name)
        self.assertEqual(result.address, self.mock_client_info_dto.address)
        self.assertEqual(result.phone, self.mock_client_info_dto.phone)
        self.assertEqual(result.email, self.mock_client_info_dto.email)
        self.assertEqual(result.order_id, self.mock_client_info_dto.order_id)

    def test_to_model_none(self):
        # Execute
        result = ClientInfoMapper.to_model(None)

        # Verify
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()