from unittest.mock import Mock

import pytest
from src.application.create_product import CreateProduct
from src.application.errors.errors import InvalidFormatError, ProductAlreadyExistsError
from src.domain.entities.product_dto import ProductDTO


class TestCreateProduct:
    def setup_method(self):
        """Set up test environment before each test method"""
        self.mock_repository = Mock()
        self.create_product_use_case = CreateProduct(self.mock_repository)

        # Sample valid product data
        self.valid_product = ProductDTO(
            id=None,
            name="Test Product",
            brand="Test Brand",
            manufacturer_id="test-manufacturer-id",
            description="Test Description",
            stock=10,
            details="{'test': 'details'}",
            storage_conditions="Test Storage Conditions",
            price=100.0,
            currency="USD",
            delivery_time=5,
            images=["image1.jpg", "image2.jpg"],
            created_at=None,
            updated_at=None
        )

    def test_create_product_successfully(self):
        """Test successful product creation"""
        # Configure mock to return None (product doesn't exist) and then a success value on add
        self.mock_repository.get_by_name.return_value = None
        self.mock_repository.add.return_value = "product-id-123"

        # Execute the use case
        result = self.create_product_use_case.execute(self.valid_product)

        # Verify repository interactions
        self.mock_repository.get_by_name.assert_called_once_with(self.valid_product.name)
        self.mock_repository.add.assert_called_once_with(self.valid_product)

        # Verify result
        assert result == "product-id-123"

    def test_invalid_price_format(self):
        """Test product creation with invalid price format"""
        # Create product with invalid price
        invalid_product = ProductDTO(
            id=None,
            name="Test Product",
            brand="Test Brand",
            manufacturer_id="test-manufacturer-id",
            description="Test Description",
            stock=10,
            details="{'test': 'details'}",
            storage_conditions="Test Storage Conditions",
            price=-150.0,  # Invalid price
            currency="USD",
            delivery_time=5,
            images=["image1.jpg", "image2.jpg"],
            created_at=None,
            updated_at=None
        )

        # Verify InvalidFormatError is raised
        with pytest.raises(InvalidFormatError):
            self.create_product_use_case.execute(invalid_product)

        # Verify repository was not called to add product
        self.mock_repository.add.assert_not_called()

    def test_non_numeric_price(self):
        """Test product creation with non-numeric price"""
        # Create product with non-numeric price
        invalid_product = ProductDTO(
            id=None,
            name="Test Product",
            brand="Test Brand",
            manufacturer_id="test-manufacturer-id",
            description="Test Description",
            stock=10,
            details="{'test': 'details'}",
            storage_conditions="Test Storage Conditions",
            price="invalid",  # Non-numeric price
            currency="USD",
            delivery_time=5,
            images=["image1.jpg", "image2.jpg"],
            created_at=None,
            updated_at=None
        )

        # Verify InvalidFormatError is raised
        with pytest.raises(InvalidFormatError):
            self.create_product_use_case.execute(invalid_product)

        # Verify repository was not called to add product
        self.mock_repository.add.assert_not_called()

    def test_invalid_delivery_time(self):
        """Test product creation with invalid delivery time"""
        # Create product with invalid delivery time
        invalid_product = ProductDTO(
            id=None,
            name="Test Product",
            brand="Test Brand",
            manufacturer_id="test-manufacturer-id",
            description="Test Description",
            stock=10,
            details="{'test': 'details'}",
            storage_conditions="Test Storage Conditions",
            price=10.00,
            currency="USD",
            delivery_time=-5, # Invalid delivery time
            images=["image1.jpg", "image2.jpg"],
            created_at=None,
            updated_at=None
        )

        # Verify InvalidFormatError is raised
        with pytest.raises(InvalidFormatError):
            self.create_product_use_case.execute(invalid_product)

        # Verify repository was not called to add product
        self.mock_repository.add.assert_not_called()

    def test_non_integer_delivery_time(self):
        """Test product creation with non-integer delivery time"""
        # Create product with non-integer delivery time
        invalid_product = ProductDTO(
            id=None,
            name="Test Product",
            brand="Test Brand",
            manufacturer_id="test-manufacturer-id",
            description="Test Description",
            stock=10,
            details="{'test': 'details'}",
            storage_conditions="Test Storage Conditions",
            price="Test Price",  # Non-integer price
            currency="USD",
            delivery_time=-5,
            images=["image1.jpg", "image2.jpg"],
            created_at=None,
            updated_at=None
        )

        # Verify InvalidFormatError is raised
        with pytest.raises(InvalidFormatError):
            self.create_product_use_case.execute(invalid_product)

        # Verify repository was not called to add product
        self.mock_repository.add.assert_not_called()

    def test_invalid_stock(self):
        """Test product creation with invalid delivery time"""
        # Create product with invalid delivery time
        invalid_product = ProductDTO(
            id=None,
            name="Test Product",
            brand="Test Brand",
            manufacturer_id="test-manufacturer-id",
            description="Test Description",
            stock=-10, # Invalid stock
            details="{'test': 'details'}",
            storage_conditions="Test Storage Conditions",
            price=10.00,
            currency="USD",
            delivery_time=5,
            images=["image1.jpg", "image2.jpg"],
            created_at=None,
            updated_at=None
        )

        # Verify InvalidFormatError is raised
        with pytest.raises(InvalidFormatError):
            self.create_product_use_case.execute(invalid_product)

        # Verify repository was not called to add product
        self.mock_repository.add.assert_not_called()

    def test_non_integer_stock(self):
        """Test product creation with non-integer delivery time"""
        # Create product with non-integer delivery time
        invalid_product = ProductDTO(
            id=None,
            name="Test Product",
            brand="Test Brand",
            manufacturer_id="test-manufacturer-id",
            description="Test Description",
            stock="invalid", # Non-integer stock
            details="{'test': 'details'}",
            storage_conditions="Test Storage Conditions",
            price="Test Price",  # Non-integer price
            currency="USD",
            delivery_time=5,
            images=["image1.jpg", "image2.jpg"],
            created_at=None,
            updated_at=None
        )

        # Verify InvalidFormatError is raised
        with pytest.raises(InvalidFormatError):
            self.create_product_use_case.execute(invalid_product)

        # Verify repository was not called to add product
        self.mock_repository.add.assert_not_called()

    def test_product_already_exists(self):
        """Test creating a product that already exists"""
        # Configure mock to return an existing product
        self.mock_repository.get_by_name.return_value = self.valid_product

        # Verify ProductAlreadyExistsError is raised
        with pytest.raises(ProductAlreadyExistsError):
            self.create_product_use_case.execute(self.valid_product)

        # Verify repository was called to check for existing product but not to add product
        self.mock_repository.get_by_name.assert_called_once_with(self.valid_product.name)
        self.mock_repository.add.assert_not_called()
