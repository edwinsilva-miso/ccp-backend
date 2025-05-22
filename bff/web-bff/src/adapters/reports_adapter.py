import logging
import os

import requests

from .products_adapter import ProductsAdapter

CLIENTS_API_URL = os.environ.get('CLIENTS_API_URL', 'http://localhost:5100')

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)

logger = logging.getLogger(__name__)


class ReportsAdapter:
    """
    Adapter for handling reports-related API calls.
    """

    def get_report_by_user_id(self, jwt, user_id):
        """
        Get a report by ID.
        :param jwt: JWT token for authorization.
        :param user_id: ID of the user to retrieve the report for.
        :return: The report data
        """
        logger.debug(f"Getting report by user ID {user_id}")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.get(f"{CLIENTS_API_URL}/api/v1/reports/{user_id}", headers=headers)
        logger.debug(f"Response received from API: {response.json()}")
        return response.json(), response.status_code

    def generate_report(self, jwt, data):
        """
        Generate a report.
        :param jwt: JWT token for authorization.
        :param data: Data to generate the report with.
        :return: The report data
        """
        logger.debug(f"Generating report with data {data}")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.post(f"{CLIENTS_API_URL}/api/v1/reports/generate", headers=headers, json=data)
        logger.debug(f"Response received from API: {response.json()}")

        report_data = None
        if response.status_code == 200 and data.get('type') == 'PRODUCTOS_MAS_VENDIDOS':
            report_data = response.json()
            report_data = self._decorate_products_report(jwt, report_data)
            logger.debug(f"Report decorated: {report_data}")

        return report_data, response.status_code

    def _decorate_products_report(self, jwt, report_data):
        """
        Decorate the order with product details.
        :param order_data: The order data
        :return: The decorated order data
        """
        logger.debug(f"Decorating products from report {report_data.get('id')}")
        product_adapter = ProductsAdapter()
        data = report_data.get('reportData', [])

        for item in data:
            product_data, _ = product_adapter.get_product_by_id(jwt, item['productId'])
            item['productName'] = product_data.get('name')

        return report_data
