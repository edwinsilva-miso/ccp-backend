import logging
import os

import requests

ROUTES_API_URL = os.environ.get('ROUTES_API_URL', 'http://localhost:5100')

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)

logger = logging.getLogger(__name__)


class RoutesAdapter:
    @staticmethod
    def create_route(jwt, route_data):
        logger.debug(f"creating a route with data {route_data}")

        response = requests.post(
            url=f"{ROUTES_API_URL}/api/v1/routes",
            headers={'Authorization': f'Bearer {jwt}'},
            json=route_data
        )

        logger.debug(f"response received from routes api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def get_user_routes_by_date(jwt, user_id, parsed_date):
        logger.debug(f"getting user::{user_id} routes by date")

        params = {"user_id": user_id}

        if parsed_date:
            params["due_to"] = parsed_date.isoformat()

        response = requests.get(
            url=f"{ROUTES_API_URL}/api/v1/routes",
            headers={'Authorization': f'Bearer {jwt}'},
            params=params
        )

        logger.debug(f"response received from routes api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def get_route_by_id(jwt, route_id):
        logger.debug(f"getting route with ID: {route_id}")

        response = requests.get(
            url=f"{ROUTES_API_URL}/api/v1/routes/{route_id}",
            headers={'Authorization': f'Bearer {jwt}'}
        )

        logger.debug(f"response received from routes api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def update_route_by_id(jwt, route_id, route_data):
        logger.debug(f"updating route with ID: {route_id} with data: {route_data}")

        response = requests.put(
            url=f"{ROUTES_API_URL}/api/v1/routes/{route_id}",
            headers={'Authorization': f'Bearer {jwt}'},
            json=route_data
        )

        logger.debug(f"response received from routes api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def delete_route_by_id(jwt, route_id):
        logger.debug(f"deleting route with ID: {route_id}")

        response = requests.delete(
            url=f"{ROUTES_API_URL}/api/v1/routes/{route_id}",
            headers={'Authorization': f'Bearer {jwt}'}
        )

        logger.debug(f"response received from routes api: status {response.status_code}")

        if response.content:
            return response.json(), response.status_code
        else:
            return {"msg": "route deleted successfully."}, response.status_code
