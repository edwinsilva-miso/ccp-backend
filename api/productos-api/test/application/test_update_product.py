from datetime import datetime
from unittest.mock import Mock

import pytest
from src.application.errors.errors import InvalidFormatError, ProductNotExistsError
from src.application.update_product import UpdateProduct
from src.domain.entities.product_dto import ProductDTO


class TestUpdateProduct:
    def setup_method(self):
        """Set up test environment before each test method"""
        self.mock_repository = Mock()
        self.update_product_use_case = UpdateProduct(self.mock_repository)

        # Sample product ID
        self.product_id = "test-product-id-123"

        # Sample valid product data
        self.valid_product = ProductDTO(
            id=self.product_id,
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
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

    def test_update_product_successfully(self):
        """Test successful product update"""
        # Configure mock to return an existing product
        existing_product = Mock()
        self.mock_repository.get_by_id.return_value = existing_product

        # Execute the use case
        result = self.update_product_use_case.execute(self.product_id, self.valid_product)

        # Verify repository interactions
        self.mock_repository.get_by_id.assert_called_once_with(self.product_id)
        self.mock_repository.update.assert_called_once_with(self.valid_product)

        # Ensure the update method was called and returned the expected result
        assert result == self.mock_repository.update.return_value

    def test_update_nonexistent_product(self):
        """Test updating a product that doesn't exist"""
        # Configure mock to return None (product doesn't exist)
        self.mock_repository.get_by_id.return_value = None

        # Verify ProductNotExistsError is raised
        with pytest.raises(ProductNotExistsError):
            self.update_product_use_case.execute(self.product_id, self.valid_product)

        # Verify repository interactions
        self.mock_repository.get_by_id.assert_called_once_with(self.product_id)
        self.mock_repository.update.assert_not_called()

    def test_invalid_price_format(self):
        """Test product update with invalid price format"""
        # Configure mock to return an existing product
        existing_product = Mock()
        self.mock_repository.get_by_id.return_value = existing_product

        # Create product with invalid price
        invalid_product = ProductDTO(
            id=self.product_id,
            name="Test Product",
            brand="Test Brand",
            manufacturer_id="test-manufacturer-id",
            description="Test Description",
            stock=10,
            details="{'test': 'details'}",
            storage_conditions="Test Storage Conditions",
            price=-150.0,  # Invalid negative price
            currency="USD",
            delivery_time=5,
            images=["image1.jpg", "image2.jpg"],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        # Verify InvalidFormatError is raised
        with pytest.raises(InvalidFormatError):
            self.update_product_use_case.execute(self.product_id, invalid_product)

        # Verify repository was not called to update product
        self.mock_repository.update.assert_not_called()

    def test_non_numeric_price(self):
        """Test product update with non-numeric price"""
        # Configure mock to return an existing product
        existing_product = Mock()
        self.mock_repository.get_by_id.return_value = existing_product

        # Create product with non-numeric price
        invalid_product = ProductDTO(
            id=self.product_id,
            name="Test Product",
            brand="Test Brand",
            manufacturer_id="test-manufacturer-id",
            description="Test Description",
            stock=10,
            details="{'test': 'details'}",
            storage_conditions="Test Storage Conditions",
            price="invalid", # Non-numeric price
            currency="USD",
            delivery_time=5,
            images=["image1.jpg", "image2.jpg"],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        # Verify InvalidFormatError is raised
        with pytest.raises(InvalidFormatError):
            self.update_product_use_case.execute(self.product_id, invalid_product)

        # Verify repository was not called to update product
        self.mock_repository.update.assert_not_called()

    def test_invalid_delivery_time(self):
        """Test product update with invalid delivery time"""
        # Configure mock to return an existing product
        existing_product = Mock()
        self.mock_repository.get_by_id.return_value = existing_product

        # Create product with invalid delivery time
        invalid_product = ProductDTO(
            id=self.product_id,
            name="Test Product",
            brand="Test Brand",
            manufacturer_id="test-manufacturer-id",
            description="Test Description",
            stock=10,
            details="{'test': 'details'}",
            storage_conditions="Test Storage Conditions",
            price=100.0,
            currency="USD",
            delivery_time=-5, # Invalid negative delivery time
            images=["image1.jpg", "image2.jpg"],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        # Verify InvalidFormatError is raised
        with pytest.raises(InvalidFormatError):
            self.update_product_use_case.execute(self.product_id, invalid_product)

        # Verify repository was not called to update product
        self.mock_repository.update.assert_not_called()

    def test_non_integer_delivery_time(self):
        """Test product update with non-integer delivery time"""
        # Configure mock to return an existing product
        existing_product = Mock()
        self.mock_repository.get_by_id.return_value = existing_product

        # Create product with non-integer delivery time
        invalid_product = ProductDTO(
            id=self.product_id,
            name="Test Product",
            brand="Test Brand",
            manufacturer_id="test-manufacturer-id",
            description="Test Description",
            stock=10,
            details="{'test': 'details'}",
            storage_conditions="Test Storage Conditions",
            price=100.0,
            currency="USD",
            delivery_time="invalid", # Non-integer delivery time
            images=["image1.jpg", "image2.jpg"],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        # Verify InvalidFormatError is raised
        with pytest.raises(InvalidFormatError):
            self.update_product_use_case.execute(self.product_id, invalid_product)

        # Verify repository was not called to update product
        self.mock_repository.update.assert_not_called()

    def test_invalid_stock(self):
        """Test product update with invalid delivery time"""
        # Configure mock to return an existing product
        existing_product = Mock()
        self.mock_repository.get_by_id.return_value = existing_product

        # Create product with invalid delivery time
        invalid_product = ProductDTO(
            id=self.product_id,
            name="Test Product",
            brand="Test Brand",
            manufacturer_id="test-manufacturer-id",
            description="Test Description",
            stock=-10, # Invalid stock
            details="{'test': 'details'}",
            storage_conditions="Test Storage Conditions",
            price=100.0,
            currency="USD",
            delivery_time=5,
            images=["image1.jpg", "image2.jpg"],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        # Verify InvalidFormatError is raised
        with pytest.raises(InvalidFormatError):
            self.update_product_use_case.execute(self.product_id, invalid_product)

        # Verify repository was not called to update product
        self.mock_repository.update.assert_not_called()

    def test_non_integer_stock(self):
        """Test product update with non-integer delivery time"""
        # Configure mock to return an existing product
        existing_product = Mock()
        self.mock_repository.get_by_id.return_value = existing_product

        # Create product with non-integer delivery time
        invalid_product = ProductDTO(
            id=self.product_id,
            name="Test Product",
            brand="Test Brand",
            manufacturer_id="test-manufacturer-id",
            description="Test Description",
            stock="invalid", # Non-integer stock
            details="{'test': 'details'}",
            storage_conditions="Test Storage Conditions",
            price=100.0,
            currency="USD",
            delivery_time=5,
            images=["image1.jpg", "image2.jpg"],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        # Verify InvalidFormatError is raised
        with pytest.raises(InvalidFormatError):
            self.update_product_use_case.execute(self.product_id, invalid_product)

        # Verify repository was not called to update product
        self.mock_repository.update.assert_not_called()
