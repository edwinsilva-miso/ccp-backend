class PaymentDTO:
    """
    A Data Transfer Object (DTO) for payment information.
    """

    def __init__(self, id:str, order_id:str, amount: float, card_number: str, cvv: str, expiry_date: str, currency: str):
        """
        Initialize a PaymentDTO object with the given parameters.
        :param id: The unique identifier for the payment.
        :param order_id: The unique identifier for the order associated with this payment.
        :param amount: The amount to be paid.
        :param card_number: The credit card number.
        :param cvv: The CVV code of the credit card.
        :param expiry_date: The expiration date of the credit card in 'MM/YY' format.
        :param currency: The currency of the payment (e.g., 'USD', 'EUR').
        """
        self.id = id
        self.order_id = order_id
        self.amount = amount
        self.card_number = card_number
        self.cvv = cvv
        self.expiry_date = expiry_date
        self.currency = currency
        self.payment_method = 'CREDIT_CARD'  # Assuming the payment method is always credit card for this DTO
        self.transaction_id = None
        self.status = None
        self.transaction_date = None

    def to_dict(self):
        """
        Convert the PaymentDTO object to a dictionary.
        :return: A dictionary representation of the PaymentDTO object.
        """
        return {
            'id': self.id,
            'amount': self.amount,
            'card_number': self.card_number,
            'cvv': self.cvv,
            'expiration_date': self.expiry_date,
            'currency': self.currency,
            'payment_method': self.payment_method,
            'transaction_id': self.transaction_id,
            'status': self.status,
            'transaction_date': self.transaction_date
        }
