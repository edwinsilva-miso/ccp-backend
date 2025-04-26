import unittest

import pytest
from src.application.errors.errors import ValidationApiError, InvalidFormatError
from src.application.utils.validation_utils import (
    _validate_numeric, _validate_present, _validate_present_object,
    _validate_currency, _validate_cvv, _validate_expiry_date,
    _validate_credit_card, _validate_email, _validate_order_details
)


class TestValidationUtils(unittest.TestCase):

    def test_validate_numeric_valid(self):
        # Test with valid integers and floats
        _validate_numeric(10, "testField")
        _validate_numeric(10.5, "testField")
        _validate_numeric(0, "testField")
        # No exception means test passed

    def test_validate_numeric_invalid_type(self):
        # Test with non-numeric values
        with pytest.raises(InvalidFormatError) as exc:
            _validate_numeric("123", "testField")
        assert "testField must be a number" in str(exc.value)

        with pytest.raises(InvalidFormatError):
            _validate_numeric(None, "testField")

        with pytest.raises(InvalidFormatError):
            _validate_numeric({}, "testField")

    def test_validate_numeric_negative(self):
        # Test with negative values
        with pytest.raises(InvalidFormatError) as exc:
            _validate_numeric(-5, "testField")
        assert "testField must be a positive number" in str(exc.value)

        with pytest.raises(InvalidFormatError):
            _validate_numeric(-10.5, "testField")

    def test_validate_present_object_valid(self):
        # Test with various non-None values
        _validate_present_object({}, "testField")
        _validate_present_object([], "testField")
        _validate_present_object("", "testField")
        _validate_present_object(0, "testField")
        _validate_present_object(False, "testField")

    def test_validate_present_object_invalid(self):
        # Test with None value
        with pytest.raises(ValidationApiError) as exc:
            _validate_present_object(None, "testField")
        assert "testField is required" in str(exc.value)

    def test_validate_present_valid(self):
        # Test with non-empty values
        _validate_present("test", "testField")
        _validate_present(0, "testField")
        _validate_present(False, "testField")
        _validate_present([1, 2, 3], "testField")
        _validate_present({"key": "value"}, "testField")

    def test_validate_present_invalid(self):
        # Test with None or empty strings
        with pytest.raises(ValidationApiError) as exc:
            _validate_present(None, "testField")
        assert "testField is required" in str(exc.value)

        with pytest.raises(ValidationApiError):
            _validate_present("", "testField")

        with pytest.raises(ValidationApiError):
            _validate_present("   ", "testField")

    def test_validate_currency_valid(self):
        # Test with valid 3-letter currency codes
        _validate_currency("USD", "currency")
        _validate_currency("EUR", "currency")
        _validate_currency("GBP", "currency")

    def test_validate_currency_invalid(self):
        # Test with invalid currency codes
        with pytest.raises(InvalidFormatError) as exc:
            _validate_currency("US", "currency")
        assert "currency must be a 3-letter currency code" in str(exc.value)

        with pytest.raises(InvalidFormatError):
            _validate_currency("USDD", "currency")

        with pytest.raises(InvalidFormatError):
            _validate_currency(123, "currency")

        with pytest.raises(InvalidFormatError):
            _validate_currency(None, "currency")

    def test_validate_cvv_valid(self):
        # Test with valid CVV codes
        _validate_cvv("123", "cvv")
        _validate_cvv("1234", "cvv")

    def test_validate_cvv_invalid(self):
        # Test with invalid CVV codes
        with pytest.raises(InvalidFormatError) as exc:
            _validate_cvv("12", "cvv")
        assert "cvv must be a 3 or 4 digit number" in str(exc.value)

        with pytest.raises(InvalidFormatError):
            _validate_cvv("12345", "cvv")

        with pytest.raises(InvalidFormatError):
            _validate_cvv("ABC", "cvv")

        with pytest.raises(InvalidFormatError):
            _validate_cvv(123, "cvv")

        with pytest.raises(InvalidFormatError):
            _validate_cvv(None, "cvv")

    def test_validate_expiry_date_valid(self):
        # Test with valid expiry dates
        _validate_expiry_date("01/25", "expiryDate")
        _validate_expiry_date("12/99", "expiryDate")

    def test_validate_expiry_date_invalid(self):
        # Test with invalid expiry dates
        with pytest.raises(InvalidFormatError) as exc:
            _validate_expiry_date("1/25", "expiryDate")
        assert "expiryDate must be in MM/YY format" in str(exc.value)

        with pytest.raises(InvalidFormatError):
            _validate_expiry_date("01-25", "expiryDate")

        with pytest.raises(InvalidFormatError):
            _validate_expiry_date("0125", "expiryDate")

        with pytest.raises(InvalidFormatError):
            _validate_expiry_date(12345, "expiryDate")

        with pytest.raises(InvalidFormatError):
            _validate_expiry_date(None, "expiryDate")

    def test_validate_credit_card_valid(self):
        # Test with valid credit card numbers
        _validate_credit_card("4111111111111111", "creditCard")
        _validate_credit_card("5555555555554444", "creditCard")
        _validate_credit_card("378282246310005", "creditCard")

    def test_validate_credit_card_invalid(self):
        # Test with invalid credit card numbers
        with pytest.raises(InvalidFormatError) as exc:
            _validate_credit_card("411111", "creditCard")
        assert "creditCard must be a valid credit card number" in str(exc.value)

        with pytest.raises(InvalidFormatError):
            _validate_credit_card("41111111111111111111", "creditCard")

        with pytest.raises(InvalidFormatError):
            _validate_credit_card("411111111111111A", "creditCard")

        with pytest.raises(InvalidFormatError):
            _validate_credit_card(4111111111111111, "creditCard")

        with pytest.raises(InvalidFormatError):
            _validate_credit_card(None, "creditCard")

    def test_validate_email_valid(self):
        # Test with valid email addresses
        _validate_email("test@example.com", "email")
        _validate_email("user.name+tag@example.co.uk", "email")
        _validate_email("user_name@domain-name.com", "email")

    def test_validate_email_invalid(self):
        # Test with invalid email addresses
        with pytest.raises(InvalidFormatError) as exc:
            _validate_email("testexample.com", "email")
        assert "email must be a valid email address" in str(exc.value)

        with pytest.raises(InvalidFormatError):
            _validate_email("test@", "email")

        with pytest.raises(InvalidFormatError):
            _validate_email("@example.com", "email")

        with pytest.raises(InvalidFormatError):
            _validate_email(None, "email")

    def test_validate_order_details_valid(self):
        # Test with valid order details
        valid_order_details = [
            {
                "productId": "prod123",
                "quantity": 2,
                "unitPrice": 10.0,
                "totalPrice": 20.0,
                "currency": "USD"
            },
            {
                "productId": "prod456",
                "quantity": 1,
                "unitPrice": 15.0,
                "totalPrice": 15.0,
                "currency": "USD"
            }
        ]
        _validate_order_details(valid_order_details)

    def test_validate_order_details_not_list(self):
        # Test with non-list order details
        with pytest.raises(InvalidFormatError) as exc:
            _validate_order_details({}, "orderDetails")
        assert "orderDetails must be an array" in str(exc.value)

        with pytest.raises(InvalidFormatError):
            _validate_order_details("not a list", "orderDetails")

    def test_validate_order_details_empty(self):
        # Test with empty order details list
        with pytest.raises(ValidationApiError) as exc:
            _validate_order_details([], "orderDetails")
        assert "orderDetails cannot be empty" in str(exc.value)

    def test_validate_order_details_invalid_item(self):
        # Test with non-dict item in order details
        with pytest.raises(InvalidFormatError) as exc:
            _validate_order_details(["not a dict"], "orderDetails")
        assert "orderDetails[0] must be an object" in str(exc.value)

    def test_validate_order_details_missing_fields(self):
        # Test with missing required fields
        with pytest.raises(ValidationApiError) as exc:
            _validate_order_details([{"productId": "prod123"}], "orderDetails")
        assert "quantity is required" in str(exc.value)

        with pytest.raises(ValidationApiError):
            _validate_order_details([{
                "quantity": 2,
                "unitPrice": 10.0,
                "totalPrice": 20.0,
                "currency": "USD"
            }], "orderDetails")

    def test_validate_order_details_invalid_fields(self):
        # Test with invalid field values
        with pytest.raises(InvalidFormatError) as exc:
            _validate_order_details([{
                "productId": "prod123",
                "quantity": "invalid",
                "unitPrice": 10.0,
                "totalPrice": 20.0,
                "currency": "USD"
            }], "orderDetails")
        assert "orderDetails[0].quantity must be a number" in str(exc.value)

        with pytest.raises(InvalidFormatError):
            _validate_order_details([{
                "productId": "prod123",
                "quantity": 2,
                "unitPrice": 10.0,
                "totalPrice": 20.0,
                "currency": "US"  # Invalid currency
            }], "orderDetails")

    def test_validate_order_details_price_mismatch(self):
        # Test with total price not matching quantity * unit price
        with pytest.raises(InvalidFormatError) as exc:
            _validate_order_details([{
                "productId": "prod123",
                "quantity": 2,
                "unitPrice": 10.0,
                "totalPrice": 25.0,  # Should be 20.0
                "currency": "USD"
            }], "orderDetails")
        assert "orderDetails[0].totalPrice must equal quantity * unitPrice" in str(exc.value)


if __name__ == '__main__':
    unittest.main()
