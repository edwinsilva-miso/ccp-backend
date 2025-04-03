import logging
import os

import requests

USERS_API_URL = os.environ.get('USERS_API_URL', 'http://localhost:5100')

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)

logger = logging.getLogger(__name__)


class UsersAdapter:

    def create_user(self, user_data):
        """
        Create a new user.
        :param user_data: Dictionary containing user data.
        :return: The created user object.
        """
        logger.debug(f"Creating user with data: {user_data['name']}, {user_data['email']}, {user_data['role']}")
        response = requests.post(f"{USERS_API_URL}/api/v1/users", json=user_data)
        logger.debug(f"Response received from API: {response.json()}")
        return response.json(), response.status_code
