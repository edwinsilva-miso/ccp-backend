import logging
import os

import requests

DELIVERIES_API_URL = os.environ.get('DELIVERIES_API_URL', 'http://localhost:5000')

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)

logger = logging.getLogger(__name__)


class DeliveriesAdapter:
    @staticmethod
    def get_customer_deliveries(jwt, customer_id):
        logger.debug(f"getting deliveries for customer with ID: {customer_id}")

        response = requests.get(
            url=f"{DELIVERIES_API_URL}/api/deliveries/customers/{customer_id}",
            headers={'Authorization': f'Bearer {jwt}'}
        )

        logger.debug(f"response received from entregas api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def get_delivery_for_customer(jwt, delivery_id, customer_id):
        logger.debug(f"getting delivery with ID: {delivery_id} for customer: {customer_id}")

        response = requests.get(
            url=f"{DELIVERIES_API_URL}/api/deliveries/{delivery_id}",
            headers={'Authorization': f'Bearer {jwt}'},
            params={'customer_id': customer_id}
        )

        logger.debug(f"response received from entregas api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def create_delivery(jwt, delivery_data):
        logger.debug(f"creating a delivery with data {delivery_data}")

        response = requests.post(
            url=f"{DELIVERIES_API_URL}/api/seller/deliveries",
            headers={'Authorization': f'Bearer {jwt}'},
            json=delivery_data
        )

        logger.debug(f"response received from entregas api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def get_seller_deliveries(jwt, seller_id):
        logger.debug(f"getting deliveries for seller with ID: {seller_id}")

        response = requests.get(
            url=f"{DELIVERIES_API_URL}/api/seller/deliveries",
            headers={'Authorization': f'Bearer {jwt}'},
            params={'seller_id': seller_id}
        )

        logger.debug(f"response received from entregas api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def get_delivery_for_seller(jwt, delivery_id, seller_id):
        logger.debug(f"getting delivery with ID: {delivery_id} for seller: {seller_id}")

        response = requests.get(
            url=f"{DELIVERIES_API_URL}/api/seller/deliveries/{delivery_id}",
            headers={'Authorization': f'Bearer {jwt}'},
            params={'seller_id': seller_id}
        )

        logger.debug(f"response received from entregas api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def update_delivery(jwt, delivery_id, delivery_data):
        logger.debug(f"updating delivery with ID: {delivery_id} with data: {delivery_data}")

        response = requests.put(
            url=f"{DELIVERIES_API_URL}/api/seller/deliveries/{delivery_id}",
            headers={'Authorization': f'Bearer {jwt}'},
            json=delivery_data
        )

        logger.debug(f"response received from entregas api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def delete_delivery(jwt, delivery_id, seller_id):
        logger.debug(f"deleting delivery with ID: {delivery_id} for seller: {seller_id}")

        response = requests.delete(
            url=f"{DELIVERIES_API_URL}/api/seller/deliveries/{delivery_id}",
            headers={'Authorization': f'Bearer {jwt}'},
            params={'seller_id': seller_id}
        )

        logger.debug(f"response received from entregas api: status {response.status_code}")

        if response.content:
            return response.json(), response.status_code
        else:
            return {"msg": "delivery deleted successfully."}, response.status_code

    @staticmethod
    def add_status_update(jwt, delivery_id, status_data):
        logger.debug(f"adding status update to delivery with ID: {delivery_id} with data: {status_data}")

        response = requests.post(
            url=f"{DELIVERIES_API_URL}/api/seller/deliveries/{delivery_id}/status",
            headers={'Authorization': f'Bearer {jwt}'},
            json=status_data
        )

        logger.debug(f"response received from entregas api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def update_status_update(jwt, status_update_id, status_data):
        logger.debug(f"updating status update with ID: {status_update_id} with data: {status_data}")

        response = requests.put(
            url=f"{DELIVERIES_API_URL}/api/seller/status/{status_update_id}",
            headers={'Authorization': f'Bearer {jwt}'},
            json=status_data
        )

        logger.debug(f"response received from entregas api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def delete_status_update(jwt, status_update_id, seller_id):
        logger.debug(f"deleting status update with ID: {status_update_id} for seller: {seller_id}")

        response = requests.delete(
            url=f"{DELIVERIES_API_URL}/api/seller/status/{status_update_id}",
            headers={'Authorization': f'Bearer {jwt}'},
            params={'seller_id': seller_id}
        )

        logger.debug(f"response received from entregas api: status {response.status_code}")

        if response.content:
            return response.json(), response.status_code
        else:
            return {"msg": "status update deleted successfully."}, response.status_code
