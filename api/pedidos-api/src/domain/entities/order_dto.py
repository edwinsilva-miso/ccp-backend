from datetime import datetime


class OrderDTO:
    def __init__(self, id: str, order_date: datetime, status: str, subtotal: float, taxes: float, total: float,
                 currency: str, client_id: str, payment_id: str, transaction_status: str, transaction_date: datetime,
                 transaction_id: str, order_items: list, order_history: list = None, created_at: datetime = None,
                 updated_at: datetime = None):
        """
        Order Data Transfer Object (DTO) for transferring order data between layers.
        :param id:
        :param order_date:
        :param status:
        :param subtotal:
        :param taxes:
        :param total:
        :param currency:
        :param client_id:
        :param payment_id:
        :param transaction_status:
        :param transaction_date:
        :param order_items:
        :param order_history:
        """
        self.id = id
        self.order_date = order_date
        self.status = status
        self.subtotal = subtotal
        self.taxes = taxes
        self.total = total
        self.currency = currency
        self.client_id = client_id
        self.payment_id = payment_id
        self.transaction_status = transaction_status
        self.transaction_date = transaction_date
        self.transaction_id = transaction_id
        self.order_items = order_items
        self.order_history = order_history if order_history is not None else []
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        """
        String representation of the OrderDTO.
        :return:
        """
        return f"OrderDTO(order_id={self.id}, order_date={self.order_date}, status={self.status}, subtotal={self.subtotal}, taxes={self.taxes}, total={self.total}, currency={self.currency}, client_id={self.client_id}, payment_id={self.payment_id}, transaction_status={self.transaction_status}, transaction_date={self.transaction_date}, transaction_id={self.transaction_id} order_items={self.order_items}, order_history={self.order_history})"

    def to_dict(self):
        """
        Convert the OrderDTO to a dictionary representation.
        :return:
        """
        return {
            "id": self.id,
            "date": self.order_date,
            "status": self.status,
            "subtotal": self.subtotal,
            "taxes": self.taxes,
            "total": self.total,
            "currency": self.currency,
            "clientId": self.client_id,
            "paymentId": self.payment_id,
            "transactionStatus": self.transaction_status,
            "transactionDate": self.transaction_date,
            "transactionId": self.transaction_id,
            "orderItems": [item.to_dict() for item in self.order_items] if self.order_items else None,
            "orderHistory": [history.to_dict() for history in self.order_history] if self.order_history else None,
        }
