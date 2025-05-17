import unittest
from unittest.mock import MagicMock
from src.infrastructure.mapper.client_salesman_mapper import ClientSalesmanMapper
from src.infrastructure.model.client_salesman_model import ClientSalesmanModel
from src.domain.entities.client_salesman_dto import ClientSalesmanDTO


class TestClientSalesmanMapper(unittest.TestCase):
    def setUp(self):
        # Setup test data
        self.test_id = "123"
        self.test_salesman_id = "456"
        self.test_client_id = "789"
        self.test_client_name = "Test Client"
        self.test_client_phone = "123456789"
        self.test_client_email = "test@example.com"
        self.test_address = "Test Address"
        self.test_city = "Test City"
        self.test_country = "Test Country"
        self.test_store_name = "Test Store"

        # Create sample model and DTO for testing
        self.sample_model = ClientSalesmanModel(
            id=self.test_id,
            salesman_id=self.test_salesman_id,
            client_id=self.test_client_id,
            client_name=self.test_client_name,
            client_phone=self.test_client_phone,
            client_email=self.test_client_email,
            address=self.test_address,
            city=self.test_city,
            country=self.test_country,
            store_name=self.test_store_name
        )

        self.sample_dto = ClientSalesmanDTO(
            id=self.test_id,
            salesman_id=self.test_salesman_id,
            client_id=self.test_client_id,
            client_name=self.test_client_name,
            client_phone=self.test_client_phone,
            client_email=self.test_client_email,
            address=self.test_address,
            city=self.test_city,
            country=self.test_country,
            store_name=self.test_store_name
        )

    def test_to_dto(self):
        # Test conversion from model to DTO
        result = ClientSalesmanMapper.to_dto(self.sample_model)

        self.assertIsInstance(result, ClientSalesmanDTO)
        self.assertEqual(result.id, self.test_id)
        self.assertEqual(result.salesman_id, self.test_salesman_id)
        self.assertEqual(result.client_id, self.test_client_id)
        self.assertEqual(result.client_name, self.test_client_name)
        self.assertEqual(result.client_phone, self.test_client_phone)
        self.assertEqual(result.client_email, self.test_client_email)
        self.assertEqual(result.address, self.test_address)
        self.assertEqual(result.city, self.test_city)
        self.assertEqual(result.country, self.test_country)
        self.assertEqual(result.store_name, self.test_store_name)

    def test_to_model(self):
        # Test conversion from DTO to model
        result = ClientSalesmanMapper.to_model(self.sample_dto)

        self.assertIsInstance(result, ClientSalesmanModel)
        self.assertEqual(result.id, self.test_id)
        self.assertEqual(result.salesman_id, self.test_salesman_id)
        self.assertEqual(result.client_id, self.test_client_id)
        self.assertEqual(result.client_name, self.test_client_name)
        self.assertEqual(result.client_phone, self.test_client_phone)
        self.assertEqual(result.client_email, self.test_client_email)
        self.assertEqual(result.address, self.test_address)
        self.assertEqual(result.city, self.test_city)
        self.assertEqual(result.country, self.test_country)
        self.assertEqual(result.store_name, self.test_store_name)

    def test_to_dto_list(self):
        # Test conversion from list of models to list of DTOs
        models = [self.sample_model, self.sample_model]
        result = ClientSalesmanMapper.to_dto_list(models)

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], ClientSalesmanDTO)
        self.assertIsInstance(result[1], ClientSalesmanDTO)
        self.assertEqual(result[0].id, self.test_id)
        self.assertEqual(result[1].id, self.test_id)

    def test_to_model_list(self):
        # Test conversion from list of DTOs to list of models
        dtos = [self.sample_dto, self.sample_dto]
        result = ClientSalesmanMapper.to_model_list(dtos)

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], ClientSalesmanModel)
        self.assertIsInstance(result[1], ClientSalesmanModel)
        self.assertEqual(result[0].id, self.test_id)
        self.assertEqual(result[1].id, self.test_id)

    def test_empty_list_conversions(self):
        # Test handling of empty lists
        self.assertEqual(ClientSalesmanMapper.to_dto_list([]), [])
        self.assertEqual(ClientSalesmanMapper.to_model_list([]), [])


if __name__ == '__main__':
    unittest.main()