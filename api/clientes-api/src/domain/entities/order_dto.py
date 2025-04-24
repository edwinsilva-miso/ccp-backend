import datetime


class OrderDTO:

    def __init__(self, id: str, client_id:str, quantity: int, subtotal: float, tax: float, total: float, currency: str,
                 status: str, created_at: datetime, updated_at: datetime):
        """
        Initialize an OrderDTO object with the given parameters.
        :param: id: The unique identifier of the order.
        :param: client_id: The unique identifier of the client associated with the order.
        :param quantity: The quantity of items in the order.
        :param subtotal: The subtotal amount of the order.
        :param tax: The tax amount of the order.
        :param total: The total amount of the order.
        :param currency: The currency of the order (e.g., 'USD', 'EUR').
        :param status: The status of the order (e.g., 'PENDING', 'COMPLETED').
        :param created_at: The date and time when the order was created.
        :param created_at: The date and time when the order was created.
        """
        self.id = id
        self.client_id = client_id
        self.quantity = quantity
        self.subtotal = subtotal
        self.tax = tax
        self.total = total
        self.currency = currency
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.client_info = None
        self.order_details = None
        self.payment = None

    def to_dict(self):
        """
        Convert the OrderDTO object to a dictionary.
        :return: A dictionary representation of the OrderDTO object.
        """
        return {
            "id": self.id,
            "clientId": self.client_id,
            "quantity": self.quantity,
            "subtotal": self.subtotal,
            "tax": self.tax,
            "total": self.total,
            "currency": self.currency,
            "status": self.status,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }
