import logging

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

from ..errors.errors import InvalidFormatError, ValidationApiError


def validate(order_data):
    """
    Validate the order data.
    :param order_data: The order data to validate.
    :raises ValidationApiError: If the order data is invalid.
    """
    logger.debug("Validating order data...")

    # Check if order_data is a dictionary
    if not isinstance(order_data, dict):
        logger.error("Invalid order data format: Expected a dictionary")
        raise ValidationApiError

    # order = order_data['order']
    payment = order_data['payment']
    client_info = order_data['clientInfo']
    order_details = order_data['orderDetails']

    logger.info("Validating order data fields...")
    # Validate order fields
    _validate_present(order_data.get('clientId'), 'clientId')
    _validate_present(order_data.get('quantity'), 'quantity')
    _validate_numeric(order_data.get('quantity'), 'quantity')
    _validate_present(order_data.get('subtotal'), 'subtotal')
    _validate_numeric(order_data.get('subtotal'), 'subtotal')
    _validate_present(order_data.get('tax'), 'tax')
    _validate_numeric(order_data.get('tax'), 'tax')
    _validate_present(order_data.get('total'), 'total')
    _validate_numeric(order_data.get('total'), 'total')
    _validate_present(order_data.get('currency'), 'currency')
    _validate_currency(order_data.get('currency'), 'currency')

    # Validate payment fields
    _validate_present_object(payment, 'payment')
    _validate_present(payment.get('amount'), 'payment.amount')
    _validate_numeric(payment.get('amount'), 'payment.amount')
    _validate_present(payment.get('cardNumber'), 'payment.cardNumber')
    _validate_credit_card(payment.get('cardNumber'), 'payment.cardNumber')
    _validate_present(payment.get('currency'), 'payment.currency')
    _validate_currency(payment.get('currency'), 'payment.currency')
    _validate_present(payment.get('cvv'), 'payment.cvv')
    _validate_cvv(payment.get('cvv'), 'payment.cvv')
    _validate_present(payment.get('expiryDate'), 'payment.expiryDate')
    _validate_expiry_date(payment.get('expiryDate'), 'payment.expiryDate')

    # Validate client info fields
    _validate_present_object(client_info, 'clientInfo')
    _validate_present(client_info.get('name'), 'clientInfo.name')
    _validate_present(client_info.get('address'), 'clientInfo.address')
    _validate_present(client_info.get('phone'), 'clientInfo.phone')
    _validate_present(client_info.get('email'), 'clientInfo.email')
    _validate_email(client_info.get('email'), 'clientInfo.email')

    # Validate order details fields
    _validate_order_details(order_details)

    logger.debug("Order data validation completed successfully.")


def _validate_order_details(order_details, field_name="orderDetails"):
    """
    Validate array of order details.
    :param order_details: The array of order detail objects to validate.
    :param field_name: Name of the field for error messages.
    :raises ValidationApiError: If the order details are invalid.
    :raises InvalidFormatError: If any order detail has invalid format.
    """
    if not isinstance(order_details, list):
        logger.error(f"Invalid format for {field_name}: not an array")
        raise InvalidFormatError(f"{field_name} must be an array")

    if len(order_details) == 0:
        logger.error(f"Invalid {field_name}: array is empty")
        raise ValidationApiError(f"{field_name} cannot be empty")

    for i, detail in enumerate(order_details):
        detail_prefix = f"{field_name}[{i}]"

        # Check if detail is a dictionary
        if not isinstance(detail, dict):
            logger.error(f"Invalid {detail_prefix}: not an object")
            raise InvalidFormatError(f"{detail_prefix} must be an object")

        # Validate required fields
        _validate_present(detail.get('productId'), f"{detail_prefix}.productId")
        _validate_present(detail.get('quantity'), f"{detail_prefix}.quantity")
        _validate_numeric(detail.get('quantity'), f"{detail_prefix}.quantity")
        _validate_present(detail.get('unitPrice'), f"{detail_prefix}.unitPrice")
        _validate_numeric(detail.get('unitPrice'), f"{detail_prefix}.unitPrice")
        _validate_present(detail.get('totalPrice'), f"{detail_prefix}.totalPrice")
        _validate_numeric(detail.get('totalPrice'), f"{detail_prefix}.totalPrice")
        _validate_present(detail.get('currency'), f"{detail_prefix}.currency")
        _validate_currency(detail.get('currency'), f"{detail_prefix}.currency")

        # Validate that total price equals quantity * unit price
        expected_total = detail.get('quantity') * detail.get('unitPrice')
        actual_total = detail.get('totalPrice')
        if abs(expected_total - actual_total) > 0.01:  # Allow small rounding differences
            logger.error(f"Invalid {detail_prefix}.totalPrice: calculation mismatch")
            raise InvalidFormatError(f"{detail_prefix}.totalPrice must equal quantity * unitPrice")


def _validate_numeric(value, field_name):
    """
    Validate if the value is numeric.
    :param value: The value to validate.
    :param field_name: The name of the field being validated.
    :raises InvalidFormatError: If the value is not numeric.
    """
    if not isinstance(value, (int, float)):
        logger.error(f"Invalid format for {field_name}: {value} is not numeric")
        raise InvalidFormatError(f"{field_name} must be a number")

    if value < 0:
        logger.error(f"Invalid value for {field_name}: {value} is negative")
        raise InvalidFormatError(f"{field_name} must be a positive number")


def _validate_present_object(value, field_name):
    """
    Validate if the value is present (not None).
    :param value: The value to validate.
    :param field_name: The name of the field being validated.
    :raises ValidationApiError: If the value is not present.
    """
    if value is None:
        logger.error(f"Missing required field: {field_name}")
        raise ValidationApiError(f"{field_name} is required")


def _validate_present(value, field_name):
    """
    Validate if the value is present (not None or empty).
    :param value: The value to validate.
    :param field_name: The name of the field being validated.
    :raises ValidationApiError: If the value is not present.
    """
    if value is None or (isinstance(value, str) and not value.strip()):
        logger.error(f"Missing required field: {field_name}")
        raise ValidationApiError(f"{field_name} is required")


def _validate_currency(value, field_name):
    """
    Validate if the currency is a valid string.
    :param value: The value to validate.
    :param field_name: The name of the field being validated.
    :raises InvalidFormatError: If the currency is not a valid string.
    """
    if not isinstance(value, str) or len(value) != 3:
        logger.error(f"Invalid format for {field_name}: {value} is not a valid currency")
        raise InvalidFormatError(f"{field_name} must be a 3-letter currency code")


def _validate_cvv(value, field_name):
    """
    Validate if the CVV is a valid string of digits.
    :param value: The value to validate.
    :param field_name: The name of the field being validated.
    :raises InvalidFormatError: If the CVV is not a valid string of digits.
    """
    if not isinstance(value, str) or not value.isdigit() or len(value) not in [3, 4]:
        logger.error(f"Invalid format for {field_name}: {value} is not a valid CVV")
        raise InvalidFormatError(f"{field_name} must be a 3 or 4 digit number")


def _validate_expiry_date(value, field_name):
    """
    Validate if the expiry date is in the correct format (MM/YY).
    :param value: The value to validate.
    :param field_name: The name of the field being validated.
    :raises InvalidFormatError: If the expiry date is not in the correct format.
    """
    if not isinstance(value, str) or len(value) != 5 or value[2] != '/':
        logger.error(f"Invalid format for {field_name}: {value} is not a valid expiry date")
        raise InvalidFormatError(f"{field_name} must be in MM/YY format")


def _validate_credit_card(value, field_name):
    """
    Validate if the credit card number is a valid string of digits.
    :param value: The value to validate.
    :param field_name: The name of the field being validated.
    :raises InvalidFormatError: If the credit card number is not a valid string of digits.
    """
    if not isinstance(value, str) or not value.isdigit() or len(value) < 13 or len(value) > 19:
        logger.error(f"Invalid format for {field_name}: {value} is not a valid credit card number")
        raise InvalidFormatError(f"{field_name} must be a valid credit card number")


def _validate_email(value, field_name):
    """
    Validate if the email is in the correct format.
    :param value: The value to validate.
    :param field_name: The name of the field being validated.
    :raises InvalidFormatError: If the email is not in the correct format.
    """
    import re
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not isinstance(value, str) or not re.match(email_regex, value):
        logger.error(f"Invalid format for {field_name}: {value} is not a valid email")
        raise InvalidFormatError(f"{field_name} must be a valid email address")
