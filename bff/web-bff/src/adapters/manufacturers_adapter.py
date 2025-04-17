import os
import logging

import requests

MANUFACTURERS_API_URL = os.environ.get('MANUFACTURERS_API_URL', 'http://localhost:5100')

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)

logger = logging.getLogger(__name__)


class ManufacturersAdapter:

    def get_all_manufacturers(self, jwt):
        """
        Get all manufacturers.
        :param jwt: JWT token for authorization.
        :return: The all manufacturers data
        """
        logger.debug("Getting all manufacturers")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.get(f"{MANUFACTURERS_API_URL}/api/v1/manufacturers", headers=headers)
        logger.debug(f"Response received from API: {response.json()}")
        return response.json(), response.status_code

    def get_manufacturer_by_id(self, jwt, manufacturer_id):
        """
        Get a manufacturer by ID.
        :param jwt: JWT token for authorization.
        :param manufacturer_id: ID of the manufacturer to retrieve.
        :return: The manufacturer data
        """
        logger.debug(f"Getting manufacturer by ID {manufacturer_id}")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.get(f"{MANUFACTURERS_API_URL}/api/v1/manufacturers/{manufacturer_id}", headers=headers)
        logger.debug(f"Response received from API: {response.json()}")
        return response.json(), response.status_code

    def get_manufacturer_by_nit(self, jwt, nit):
        """
        Get a manufacturer by ID.
        :param jwt: JWT token for authorization.
        :param nit: NIT of the manufacturer to retrieve.
        :return: The manufacturer data
        """
        logger.debug(f"Getting manufacturer by NIT {nit}")
        headers = {'Authorization': f'Bearer {jwt}'}
        query_params = {'nit': nit}
        response = requests.get(f"{MANUFACTURERS_API_URL}/api/v1/manufacturers/search", headers=headers, params=query_params)
        logger.debug(f"Response received from API: {response.json()}")
        return response.json(), response.status_code

    def create_manufacturer(self, jwt, manufacturer_data):
        """
        Create a new manufacturer.
        :param jwt: JWT token for authorization.
        :param manufacturer_data: Dictionary containing manufacturer data.
        :return: The created manufacturer ID.
        """
        logger.debug(f"Creating manufacturer {manufacturer_data['name']}")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.post(f"{MANUFACTURERS_API_URL}/api/v1/manufacturers", headers=headers, json=manufacturer_data)
        logger.debug(f"Response received from API: {response.json()}")
        return response.json(), response.status_code

    def update_manufacturer(self, jwt, manufacturer_id,  manufacturer_data):
        """
        Create a new manufacturer.
        :param jwt: JWT token for authorization.
        :param manufacturer_id: ID of the manufacturer to update.
        :param manufacturer_data: Dictionary containing manufacturer data.
        :return: The created manufacturer ID.
        """
        logger.debug(f"Updating manufacturer {manufacturer_data['name']}")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.put(f"{MANUFACTURERS_API_URL}/api/v1/manufacturers/{manufacturer_id}", headers=headers, json=manufacturer_data)
        logger.debug(f"Response received from API: {response.json()}")
        return response.json(), response.status_code


    def delete_manufacturer(self, jwt, manufacturer_id):
        """
        Delete a manufacturer by ID.
        :param jwt: JWT token for authorization.
        :param manufacturer_id: ID of the manufacturer to delete.
        :return: The response from the API
        """
        logger.debug("Deleting manufacturer")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.delete(f"{MANUFACTURERS_API_URL}/api/v1/manufacturers/{manufacturer_id}", headers=headers)
        if response.status_code == 204:
            return {}, response.status_code
        return response.json(), response.status_code