import datetime
from typing import Dict, List


class ProductDTO:
    def __init__(self,
                 id: str,
                 name: str,
                 brand: str,
                 manufacturer_id: str,
                 description: str,
                 stock: int,
                 details: Dict[str, str],
                 storage_conditions: str,
                 price: float,
                 currency: str,
                 delivery_time: int,
                 images: list[str],
                 created_at: datetime = None,
                 updated_at: datetime = None):
        """
        Initiates a ProductDTO instance with the given parameters.

        Args:
            id (str): The product ID.
            name (str): The product name
            manufacturer_id (str): The ID of the manufacturer.
            description (str): A short description of the product.
            stock (int): The product stock.
            details (Dict[str, str]): A dictionary ofproduct details,
                                       where the key is the characteristic name and the value is its value.
            storage_conditions (str): The product storage conditions.
            price (float): The unit price of the product.
            delivery_time (int): The delivery time of the product by days.
            images (List[str]): A URL lists referencing to images of the product.
            created_at (datetime): The creation date of the product.
            updated_at (datetime): The last update date of the product.
        """
        self.id = id
        self.name = name
        self.brand = brand
        self.manufacturer_id = manufacturer_id
        self.description = description
        self.stock = stock
        self.details = details
        self.storage_conditions = storage_conditions
        self.price = price
        self.currency = currency
        self.delivery_time = delivery_time
        self.images = images
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price}, details={self.details}), stock={self.stock}, "

    def to_dict(self):
        """
        Cast a ProductDTO instance to a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "brand": self.brand,
            "manufacturerId": self.manufacturer_id,
            "description": self.description,
            "stock": self.stock,
            "details": self.details,
            "storageConditions": self.storage_conditions,
            "price": self.price,
            "currency": self.currency,
            "deliveryTime": self.delivery_time,
            "images": self.images,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }
