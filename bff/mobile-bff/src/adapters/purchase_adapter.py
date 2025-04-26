import logging
import os
from datetime import datetime, timedelta

import requests

from .products_adapter import ProductsAdapter

CLIENTS_API_URL = os.environ.get('CLIENTS_API_URL', 'http://localhost:5101')

# Configure logging once at module level
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class PurchaseAdapter:
    def __init__(self):
        self.products_adapter = ProductsAdapter()

    def create_order(self, jwt, order_data):
        """
        Create a new order.
        :param jwt: JWT token for authorization.
        :param order_data: The order data to create.
        :return: Tuple of (order_data, status_code)
        """
        logger.debug("Creating a new order")
        headers = {'Authorization': f'Bearer {jwt}'}

        # Create the order
        response = requests.post(
            f"{CLIENTS_API_URL}/api/v1/orders",
            json=order_data,
            headers=headers
        )

        response_data = response.json()

        # Enrich product information if order was successful or pending payment
        if response.status_code in [201, 402]:
            self._enrich_product_information(jwt, response_data, response.status_code)

        logger.debug(f"Response received from API: {response_data}")
        return response_data, response.status_code

    def _enrich_product_information(self, jwt, order_data, status_code):
        """
        Enrich product information with details from products API.
        :param jwt: JWT token for authorization.
        :param order_data: The order data to enrich.
        :param status_code: The status code from the order creation.
        """
        logging.debug("Enriching product information")
        products = order_data.get('orderDetails', [])

        for product in products:
            product_id = product.get('product_id')
            product_data, response_status = self.products_adapter.get_product_by_id(jwt, product_id)

            if product_data and response_status == 200:
                # Add product information
                product['name'] = product_data.get('name')
                product['brand'] = product_data.get('brand')

                # Calculate delivery date if order was successfully created
                if status_code == 201 and 'delivery_time' in product_data:
                    delivery_date = datetime.now() + timedelta(days=product_data['delivery_time'])
                    product['deliveryTime'] = f"{product_data.get('delivery_time')} días"
                    product['deliveryDate'] = delivery_date.strftime('%Y-%m-%d')

