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

    def get_products_by_manufacturer(self, jwt, manufacturer_id):
        """
        Get all products by manufacturer.
        :param jwt: JWT token for authorization.
        :param manufacturer_id: ID of the manufacturer to retrieve products for.
        :return: The products data
        """
        logger.debug("Getting products by manufacturer")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.get(f"{PRODUCTS_API_URL}/api/v1/manufacturers/{manufacturer_id}/products",
                                headers=headers)
        logger.debug(f"Response received from API: {response.json()}")
        return response.json(), response.status_code

    def create_product(self, jwt, product_data):
        """
        Create a new product.
        :param jwt: JWT token for authorization.
        :param product_data: The product data to create.
        :return: The created product data
        """
        logger.debug("Creating a new product")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.post(f"{PRODUCTS_API_URL}/api/v1/products", headers=headers, json=product_data)
        logger.debug(f"Response received from API: {response.json()}")
        return response.json(), response.status_code

    def update_product(self, jwt, product_id, product_data):
        """
        Update an existing product.
        :param jwt: JWT token for authorization.
        :param product_id: ID of the product to update.
        :param product_data: The updated product data.
        :return: The updated product data
        """
        logger.debug(f"Updating product with ID {product_id}")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.put(f"{PRODUCTS_API_URL}/api/v1/products/{product_id}", headers=headers, json=product_data)
        logger.debug(f"Response received from API: {response.json()}")
        return response.json(), response.status_code

    def delete_product(self, jwt, product_id):
        """
        Delete a product by ID.
        :param jwt: JWT token for authorization.
        :param product_id: ID of the product to delete.
        :return: The deleted product data
        """
        logger.debug(f"Deleting product with ID {product_id}")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.delete(f"{PRODUCTS_API_URL}/api/v1/products/{product_id}", headers=headers)
        logger.debug(f"Response received from API: {response.json()}")
        if response.status_code == 204:
            return {}, response.status_code
        return response.json(), response.status_code
