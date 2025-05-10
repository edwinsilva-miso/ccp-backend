import logging
import os

import requests

SALES_API_URL = os.environ.get('SALES_API_URL', 'http://localhost:5106/api/v1/sales')

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)

logger = logging.getLogger(__name__)


class SalesmanAdapter:

    def get_clients_by_salesman(self, jwt, salesman_id):
        """
        Get all clients by salesman.
        :param jwt: JWT token for authorization.
        :param salesman_id: ID of the salesman to retrieve clients for.
        :return: The clients data
        """
        logger.debug("Getting clients by salesman")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.get(f"{SALES_API_URL}/api/v1/salesman/{salesman_id}/clients", headers=headers)
        logger.debug(f"Response received from API: {response.json()}")
        return response.json(), response.status_code

    def associate_client(self, jwt, salesman_id, client_data):
        """
        Associate a client with a salesman.
        :param jwt: JWT token for authorization.
        :param salesman_id: ID of the salesman to associate the client with.
        :param client_data: Data of the client to associate.
        :return: The associated client data
        """
        logger.debug("Associating client with salesman")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.post(f"{SALES_API_URL}/api/v1/salesman/{salesman_id}/clients", json=client_data, headers=headers)
        logger.debug(f"Response received from API: {response.json()}")
        return response.json(), response.status_code
