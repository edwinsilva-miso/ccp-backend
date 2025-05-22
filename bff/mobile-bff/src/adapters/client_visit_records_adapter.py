import logging
import os

import requests

from .salesman_adapter import SalesmanAdapter

SALES_API_URL = os.environ.get('SALES_API_URL', 'http://localhost:5106/api/v1/sales')

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)

logger = logging.getLogger(__name__)


class ClientVisitRecordsAdapter:
    """
    Adapter for ClientVisitRecordsRepository to interact with ClientVisitRecordsDAO and ClientVisitRecordsMapper.
    """

    def __init__(self):
        """
        Initialize the adapter.
        """
        self.salesman_adapter = SalesmanAdapter()

    def get_client_visit_records(self, jwt, salesman_id):
        """
        Retrieves all visit records for a given client.
        :param jwt: JWT token for authorization.
        :param salesman_id: ID of the salesman to retrieve
        :return: The visit records data
        """
        logger.debug("Getting client visit records")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.get(f"{SALES_API_URL}/api/v1/salesman/{salesman_id}/visits", headers=headers)
        logger.debug(f"Response received from API: {response.json()}")
        if response.status_code == 200:
            records = response.json()
            # Decorate the response
            decorated_records = [self._decorate_response(jwt, record) for record in records]
            return decorated_records, response.status_code
        return response.json(), response.status_code

    def get_client_visit_record(self, jwt, salesman_id, record_id):
        """
        Retrieves all visit records for a given client.
        :param jwt: JWT token for authorization.
        :param salesman_id: ID of the salesman to retrieve
        :param record_id: ID of the visit record to retrieve
        :return: The visit records data
        """
        logger.debug(f"Getting client visit record: {record_id}")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.get(f"{SALES_API_URL}/api/v1/salesman/{salesman_id}/visits/{record_id}", headers=headers)
        logger.debug(f"Response received from API: {response.json()}")
        if response.status_code == 200:
            record = response.json()
            # Decorate the response
            decorated_record = self._decorate_response(jwt, record)
            return decorated_record, response.status_code
        else:
            return response.json(), response.status_code

    def add_client_visit_record(self, jwt, salesman_id, data):
        """
        Adds a new visit record for a client.
        :param jwt: JWT token for authorization.
        :param salesman_id: ID of the salesman to add the visit record for.
        :param data: Data of the visit record to add.
        :return: The added visit record data
        """
        logger.debug("Adding client visit record")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.post(f"{SALES_API_URL}/api/v1/salesman/{salesman_id}/visits", json=data, headers=headers)
        logger.debug(f"Response received from API: {response.json()}")
        return response.json(), response.status_code

    def _decorate_response(self, jwt, record):
        """
        Decorates the response from the API.
        :param record: The record to decorate.
        :return: The decorated response.
        """
        salesman_id = record.get('salesmanId')
        client_id = record.get('clientId')
        clients = self.salesman_adapter.get_clients_by_salesman(jwt, salesman_id)
        if clients and len(clients) > 0:
            clients_data = clients[0]
            client_dict = {client.get('clientId'): client for client in clients_data}
            if client_id in client_dict:
                matching_client = client_dict[client_id]
                record['clientName'] = matching_client['clientName']
                record['store'] = matching_client['storeName']

        return record
