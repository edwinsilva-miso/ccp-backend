import logging
import os

import requests

PRODUCTS_API_URL = os.environ.get('PRODUCTS_API_URL', 'http://localhost:5100')

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)

logger = logging.getLogger(__name__)


class ProductsAdapter:
    def get_all_products(self, jwt):
        """
        Get all products.
        :param jwt: JWT token for authorization.
        :return: The all products data
        """
        logger.debug("Getting all products")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.get(f"{PRODUCTS_API_URL}/api/v1/products", headers=headers)
        logger.debug(f"Response received from API: {response.json()}")
        return response.json(), response.status_code

    def get_product_by_id(self, jwt, product_id):
        """
        Get a product by ID.
        :param jwt: JWT token for authorization.
        :param product_id: ID of the product to retrieve.
        :return: The product data
        """
        logger.debug(f"Getting product by ID {product_id}")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.get(f"{PRODUCTS_API_URL}/api/v1/products/{product_id}", headers=headers)
        logger.debug(f"Response received from API: {response.json()}")
        return response.json(), response.status_code
