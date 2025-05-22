class OrderDetailsDTO:

    def __init__(self, id: str, order_id: str, product_id: int, quantity: int, unit_price: float, total_price: float,
                 currency: str):
        """
        Initialize an OrderDetailDTO object with the given parameters.
        :param id: The unique identifier for the order detail.
        :param order_id: The unique identifier for the order.
        :param product_id: The unique identifier for the product.
        :param quantity: The quantity of the product in the order.
        :param unit_price: The price per unit of the product.
        :param total_price: The total price for the quantity of the product.
        :param currency: The currency of the price (e.g., 'USD', 'EUR').
        """
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = total_price
        self.currency = currency

    def to_dict(self):
        """
        Convert the OrderDetailDTO object to a dictionary.
        :return: A dictionary representation of the OrderDetailDTO object.
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
