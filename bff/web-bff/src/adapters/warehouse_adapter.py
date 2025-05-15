import logging
import os

import requests

WAREHOUSES_API_URL = os.environ.get('WAREHOUSES_API_URL', 'http://localhost:5069')

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)

logger = logging.getLogger(__name__)


class WarehouseAdapter:
    @staticmethod
    def create_warehouse(jwt, warehouse_data):
        logger.debug(f"creating a warehouse with data {warehouse_data}")

        response = requests.post(
            url=f"{WAREHOUSES_API_URL}/api/v1/warehouses",
            headers={'Authorization': f'Bearer {jwt}'},
            json=warehouse_data
        )

        logger.debug(f"response received from bodegas api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def get_warehouse_by_id(jwt, warehouse_id):
        logger.debug(f"getting warehouse with ID: {warehouse_id}")

        response = requests.get(
            url=f"{WAREHOUSES_API_URL}/api/v1/warehouses/{warehouse_id}",
            headers={'Authorization': f'Bearer {jwt}'}
        )

        logger.debug(f"response received from bodegas api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def get_all_warehouses(jwt, administrator_id: str = None):
        logger.debug(f"getting all warehouses")

        params = {}
        if administrator_id:
            params = {"administrator_id": administrator_id}

        response = requests.get(
            url=f"{WAREHOUSES_API_URL}/api/v1/warehouses",
            headers={'Authorization': f'Bearer {jwt}'},
            params=params
        )

        logger.debug(f"response received from bodegas api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def update_warehouse_by_id(jwt, warehouse_id, warehouse_data):
        logger.debug(f"updating warehouse with ID: {warehouse_id} with data: {warehouse_data}")

        response = requests.put(
            url=f"{WAREHOUSES_API_URL}/api/v1/warehouses/{warehouse_id}",
            headers={'Authorization': f'Bearer {jwt}'},
            json=warehouse_data
        )

        logger.debug(f"response received from bodegas api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def delete_warehouse_by_id(jwt, warehouse_id):
        logger.debug(f"deleting warehouse with ID: {warehouse_id}")

        response = requests.delete(
            url=f"{WAREHOUSES_API_URL}/api/v1/warehouses/{warehouse_id}",
            headers={'Authorization': f'Bearer {jwt}'}
        )

        logger.debug(f"response received from bodegas api: status {response.status_code}")

        if response.content:
            return response.json(), response.status_code
        else:
            return {"msg": "warehouse deleted successfully."}, response.status_code
