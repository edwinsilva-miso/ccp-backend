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


class ClientsAdapter:
    def __init__(self):
        self.products_adapter = ProductsAdapter()

    def create_order(self, jwt, order_data, salesman_id=None):
        """
        Create a new order.
        :param jwt: JWT token for authorization.
        :param order_data: The order data to create.
        :param salesman_id: Optional salesman ID to associate with the order.
        :return: Tuple of (order_data, status_code)
        """
        logger.debug("Creating a new order")
        headers = {'Authorization': f'Bearer {jwt}'}

        if salesman_id:
            headers['salesman-id'] = salesman_id

        # Create the order
        response = requests.post(
            f"{CLIENTS_API_URL}/api/v1/clients/orders",
            json=order_data,
            headers=headers
        )

        response_data = response.json()

        # Enrich product information if order was successful or pending payment
        if response.status_code in [201, 402]:
            self._enrich_product_information(jwt, response_data, response.status_code)

        logger.debug(f"Response received from API: {response_data}")
        return response_data, response.status_code

    def lists_orders(self, jwt, client_id):
        """
        List orders for a specific client.
        :param jwt: JWT token for authorization.
        :param client_id: The ID of the client to list orders for.
        :return: Tuple of (orders_data, status_code)
        """
        logger.debug("Listing orders for client")
        headers = {'Authorization': f'Bearer {jwt}'}
        params = {'clientId': client_id}

        # List the orders
        response = requests.get(
            f"{CLIENTS_API_URL}/api/v1/clients/orders",
            headers=headers,
            params=params
        )

        response_data = response.json()

        logger.debug(f"Response received from API: {response_data}")
        return response_data, response.status_code

    def get_order_by_id(self, jwt, order_id):
        """
        Get order details by order ID.
        :param jwt: JWT token for authorization.
        :param order_id: The ID of the order to retrieve.
        :return: Tuple of (order_data, status_code)
        """
        logger.debug("Getting order by ID")
        headers = {'Authorization': f'Bearer {jwt}'}

        # Get the order details
        response = requests.get(
            f"{CLIENTS_API_URL}/api/v1/clients/orders/{order_id}",
            headers=headers
        )

        response_data = response.json()

        # Enrich product information if order was successful or pending payment
        if response.status_code == 200:
            self._enrich_product_information(jwt, response_data, response.status_code)

        logger.debug(f"Response received from API: {response_data}")
        return response_data, response.status_code

    def get_orders_by_salesman_id(self, jwt, salesman_id):
        """
        Get orders by salesman ID.
        :param jwt: JWT token for authorization
        :param salesman_id: The ID of the salesman to retrieve
        :return: Tuple of (orders_data, status_code)
        """
        logger.debug("Listing orders for salesman_id")
        headers = {'Authorization': f'Bearer {jwt}'}


        # List the orders
        response = requests.get(
            f"{CLIENTS_API_URL}/api/v1/clients/orders/salesman/{salesman_id}",
            headers=headers
        )

        response_data = response.json()

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
            product_id = product.get('productId')
            product_data, response_status = self.products_adapter.get_product_by_id(jwt, product_id)

            if product_data and response_status == 200:
                # Add product information
                product['name'] = product_data.get('name')
                product['brand'] = product_data.get('brand')

                # Calculate delivery date if order was successfully created
                if status_code in [200, 201] and 'deliveryTime' in product_data:
                    delivery_date = datetime.now() + timedelta(days=product_data['deliveryTime'])
                    product['deliveryTime'] = f"{product_data.get('deliveryTime')} días"
                    product['deliveryDate'] = delivery_date.strftime('%Y-%m-%d')
