import unittest
import json
from src.domain.mapper.products_json_mapper import ProductsJsonMapper
from src.domain.entities.product_dto import ProductDTO


class TestProductsJsonMapper(unittest.TestCase):

    def test_valid_products_conversion(self):
        # Arrange
        test_products = [
            {
                'manufacturer_id': '123',
                'name': 'Test Product',
                'brand': 'Test Brand',
                'description': 'Test Description',
                'stock': 10,
                'details': json.dumps({'weight': '1kg', 'color': 'red'}),
                'storage_conditions': 'Cool and dry',
                'price': 100.0,
                'currency': 'USD',
                'delivery_time': '3-5 days',
                'images': json.dumps(['img1.jpg', 'img2.jpg'])
            }
        ]

        # Act
        result = ProductsJsonMapper.from_json_to_dto_list(test_products)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], ProductDTO)
        self.assertEqual(result[0].manufacturer_id, '123')
        self.assertEqual(result[0].name, 'Test Product')
        self.assertEqual(result[0].brand, 'Test Brand')
        self.assertEqual(result[0].details, {'weight': '1kg', 'color': 'red'})
        self.assertEqual(result[0].images, ['img1.jpg', 'img2.jpg'])

    def test_empty_list(self):
        # Arrange
        test_products = []

        # Act
        result = ProductsJsonMapper.from_json_to_dto_list(test_products)

        # Assert
        self.assertEqual(result, [])

    def test_details_already_dict(self):
        # Arrange
        test_products = [
            {
                'manufacturer_id': '123',
                'name': 'Test Product',
                'brand': 'Test Brand',
                'description': 'Test Description',
                'stock': 10,
                'details': {'weight': '1kg', 'color': 'red'},  # Already a dict
                'storage_conditions': 'Cool and dry',
                'price': 100.0,
                'currency': 'USD',
                'delivery_time': '3-5 days',
                'images': json.dumps(['img1.jpg', 'img2.jpg'])
            }
        ]

        # Act
        result = ProductsJsonMapper.from_json_to_dto_list(test_products)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].details, {'weight': '1kg', 'color': 'red'})

    def test_images_already_list(self):
        # Arrange
        test_products = [
            {
                'manufacturer_id': '123',
                'name': 'Test Product',
                'brand': 'Test Brand',
                'description': 'Test Description',
                'stock': 10,
                'details': json.dumps({'weight': '1kg', 'color': 'red'}),
                'storage_conditions': 'Cool and dry',
                'price': 100.0,
                'currency': 'USD',
                'delivery_time': '3-5 days',
                'images': ['img1.jpg', 'img2.jpg']  # Already a list
            }
        ]

        # Act
        result = ProductsJsonMapper.from_json_to_dto_list(test_products)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].images, ['img1.jpg', 'img2.jpg'])

    def test_invalid_product_skipped(self):
        # Arrange
        test_products = [
            {
                'manufacturer_id': '123',
                'name': 'Valid Product',
                'brand': 'Test Brand',
                'description': 'Test Description',
                'stock': 10,
                'details': json.dumps({'weight': '1kg'}),
                'storage_conditions': 'Cool and dry',
                'price': 100.0,
                'currency': 'USD',
                'delivery_time': '3-5 days',
                'images': json.dumps(['img1.jpg'])
            },
            {
                'manufacturer_id': '456',
                'name': 'Invalid Product',
                'details': 'invalid json {',  # Invalid JSON
                'images': json.dumps(['img1.jpg'])
            }
        ]

        # Act
        result = ProductsJsonMapper.from_json_to_dto_list(test_products)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, 'Valid Product')

    def test_missing_fields(self):
        # Arrange
        test_products = [
            {
                'manufacturer_id': '123',
                'name': 'Minimal Product',
                # Missing many fields
                'details': json.dumps({}),
                'images': json.dumps([])
            }
        ]

        # Act
        result = ProductsJsonMapper.from_json_to_dto_list(test_products)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].manufacturer_id, '123')
        self.assertEqual(result[0].name, 'Minimal Product')
        self.assertIsNone(result[0].brand)
        self.assertIsNone(result[0].description)


if __name__ == '__main__':
    unittest.main()