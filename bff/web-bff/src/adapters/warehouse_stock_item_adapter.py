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


class WarehouseStockItemAdapter:
    @staticmethod
    def create_warehouse_stock_item(jwt, warehouse_stock_item_data):
        logger.debug(f"creating a warehouse stock item with data {warehouse_stock_item_data}")

        response = requests.post(
            url=f"{WAREHOUSES_API_URL}/api/v1/warehouse-stock-items",
            headers={'Authorization': f'Bearer {jwt}'},
            json=warehouse_stock_item_data
        )

        logger.debug(f"response received from bodegas api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def get_warehouse_stock_item_by_id(jwt, item_id):
        logger.debug(f"getting warehouse stock item with ID: {item_id}")

        response = requests.get(
            url=f"{WAREHOUSES_API_URL}/api/v1/warehouse-stock-items/{item_id}",
            headers={'Authorization': f'Bearer {jwt}'}
        )

        logger.debug(f"response received from bodegas api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def get_warehouse_stock_items_by_warehouse(jwt, warehouse_id):
        logger.debug(f"getting all warehouse stock items for warehouse ID: {warehouse_id}")

        response = requests.get(
            url=f"{WAREHOUSES_API_URL}/api/v1/warehouse-stock-items/warehouse/{warehouse_id}",
            headers={'Authorization': f'Bearer {jwt}'}
        )

        logger.debug(f"response received from bodegas api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def update_warehouse_stock_item_by_id(jwt, item_id, warehouse_stock_item_data):
        logger.debug(f"updating warehouse stock item with ID: {item_id} with data: {warehouse_stock_item_data}")

        response = requests.put(
            url=f"{WAREHOUSES_API_URL}/api/v1/warehouse-stock-items/{item_id}",
            headers={'Authorization': f'Bearer {jwt}'},
            json=warehouse_stock_item_data
        )

        logger.debug(f"response received from bodegas api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def delete_warehouse_stock_item_by_id(jwt, item_id):
        logger.debug(f"deleting warehouse stock item with ID: {item_id}")

        response = requests.delete(
            url=f"{WAREHOUSES_API_URL}/api/v1/warehouse-stock-items/{item_id}",
            headers={'Authorization': f'Bearer {jwt}'}
        )

        logger.debug(f"response received from bodegas api: status {response.status_code}")

        if response.content:
            return response.json(), response.status_code
        else:
            return {"msg": "warehouse stock item deleted successfully."}, response.status_code