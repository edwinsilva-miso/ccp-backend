import logging
import os
import requests

SALES_API_URL = os.environ.get('SALES_API_URL', 'http://localhost:5200')

logger = logging.getLogger(__name__)

class SellingPlanAdapter:
    @staticmethod
    def create_selling_plan(jwt, plan_data):
        logger.debug(f"Creating selling plan with data: {plan_data}")
        response = requests.post(
            url=f"{SALES_API_URL}/api/v1/selling-plans",
            headers={'Authorization': f'Bearer {jwt}'},
            json=plan_data
        )
        logger.debug(f"Response from selling plans API: {response.json()}")
        return response.json(), response.status_code

    @staticmethod
    def update_selling_plan(jwt, plan_id, plan_data):
        logger.debug(f"Updating selling plan with ID: {plan_id}, data: {plan_data}")
        response = requests.put(
            url=f"{SALES_API_URL}/api/v1/selling-plans/{plan_id}",
            headers={'Authorization': f'Bearer {jwt}'},
            json=plan_data
        )
        logger.debug(f"Response from selling plans API: {response.json()}")
        return response.json(), response.status_code

    @staticmethod
    def get_selling_plan(jwt, plan_id):
        logger.debug(f"Getting selling plan with ID: {plan_id}")
        response = requests.get(
            url=f"{SALES_API_URL}/api/v1/selling-plans/{plan_id}",
            headers={'Authorization': f'Bearer {jwt}'}
        )
        logger.debug(f"Response from selling plans API: {response.json()}")
        return response.json(), response.status_code

    @staticmethod
    def get_selling_plans_by_user(jwt, user_id):
        logger.debug(f"Getting selling plans for user ID: {user_id}")
        response = requests.get(
            url=f"{SALES_API_URL}/api/v1/selling-plans/user/{user_id}",
            headers={'Authorization': f'Bearer {jwt}'}
        )
        logger.debug(f"Response from selling plans API: {response.json()}")
        return response.json(), response.status_code

    @staticmethod
    def delete_selling_plan(jwt, plan_id):
        logger.debug(f"Deleting selling plan with ID: {plan_id}")
        response = requests.delete(
            url=f"{SALES_API_URL}/api/v1/selling-plans/{plan_id}",
            headers={'Authorization': f'Bearer {jwt}'}
        )
        logger.debug(f"Response from selling plans API: status {response.status_code}")
        if response.content:
            return response.json(), response.status_code
        else:
            return {"msg": "selling plan deleted successfully."}, response.status_code