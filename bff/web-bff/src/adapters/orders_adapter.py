import logging
import os

import requests

from .products_adapter import ProductsAdapter

ORDERS_API_URL = os.environ.get('ORDERS_API_URL', 'http://localhost:5100')

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)

logger = logging.getLogger(__name__)


class OrdersAdapter:

    def list_orders(self, jwt):
        """
        List all orders.
        :param jwt: JWT token for authorization.
        :return: The orders data
        """
        logger.debug("Listing all orders")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.get(f"{ORDERS_API_URL}/api/v1/orders", headers=headers)
        logger.debug(f"Response received from API: {response.json()}")
        return response.json(), response.status_code

    def get_order_by_id(self, jwt, order_id):
        """
        Get an order by ID.
        :param jwt: JWT token for authorization.
        :param order_id: ID of the order to retrieve.
        :return: The order data
        """
        logger.debug(f"Getting order by ID {order_id}")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.get(f"{ORDERS_API_URL}/api/v1/orders/{order_id}", headers=headers)
        order_data = None
        if response.status_code == 200:
            order_data = response.json()
            order_data = self._decorate_order(jwt, order_data)
            logger.debug(f"Order decorated: {order_data}")

        logger.debug(f"Response received from API: {order_data}")
        return order_data, response.status_code

    def _decorate_order(self, jwt, order_data):
        """
        Decorate the order with product details.
        :param order_data: The order data
        :return: The decorated order data
        """
        logger.debug(f"Decorating order {order_data['id']}")
        product_adapter = ProductsAdapter()
        order_items = order_data.get('orderItems', [])

        for item in order_items:
            product_data, _ = product_adapter.get_product_by_id(jwt, item['productId'])
            item['productName'] = product_data.get('name')

        return order_data
