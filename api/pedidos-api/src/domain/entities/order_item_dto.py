class OrderItemDTO:
    def __init__(self, id: str, order_id: str, product_id: str, quantity: int, unit_price: float = 0.0,
                 total_price: float = 0.0, currency: str = "USD"):
        """
        Order Item Data Transfer Object (DTO) for transferring order item data between layers.
        :param id:
        :param order_id:
        :param product_id:
        :param quantity:
        :param unit_price:
        :param total_price:
        :param currency:
        """
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = total_price
        self.currency = currency

    def __repr__(self):
        """
        String representation of the OrderItemDTO.
        :return:
        """
        return f"OrderItemDTO(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity}, unit_price={self.unit_price}, total_price={self.total_price}, currency={self.currency})"

    def to_dict(self):
        """
        Convert the OrderItemDTO to a dictionary representation.
        :return:
        """
        return {
            "id": self.id,
            "orderId": self.order_id,
            "productId": self.product_id,
            "quantity": self.quantity,
            "unitPrice": self.unit_price,
            "totalPrice": self.total_price,
            "currency": self.currency
        }
