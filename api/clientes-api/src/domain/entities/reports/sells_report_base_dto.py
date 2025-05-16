class SellsReportBaseDTO:
    """
    SellsReportBaseDTO is a Data Transfer Object (DTO) that represents the base structure for sales reports.
    """
    def __init__(self, order_id: str, created_at: str, quantity: int, subtotal: float, tax: float, total: float, currency: str, status: str):
        """
        Initialize a SellsReportBaseDTO object with the given parameters.
        :param order_id: The unique identifier of the order.
        :param created_at: The date and time when the order was created.
        :param quantity: The quantity of items in the order.
        :param subtotal: The subtotal amount of the order.
        :param tax: The tax amount of the order.
        :param total: The total amount of the order.
        :param currency: The currency of the order (e.g., 'USD', 'EUR').
        :param status: The status of the order (e.g., 'PENDING', 'COMPLETED').
        """
        self.order_id = order_id
        self.created_at = created_at
        self.quantity = quantity
        self.subtotal = subtotal
        self.tax = tax
        self.total = total
        self.currency = currency
        self.status = status

    def to_dict(self):
        """
        Convert the SellsReportBaseDTO object to a dictionary.
        :return: A dictionary representation of the SellsReportBaseDTO object.
        """
        return {
            "orderId": self.order_id,
            "createdAt": self.created_at,
            "quantity": self.quantity,
            "subtotal": self.subtotal,
            "tax": self.tax,
            "total": self.total,
            "currency": self.currency,
            "status": self.status
        }