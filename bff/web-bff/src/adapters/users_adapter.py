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

    def authorize(self, email, password):
        """
        Authorize a user and get their token.
        :param email: User's email.
        :param password: User's password.
        :return: The user's token and expiration date.
        """
        logger.debug(f"Authorizing user with email: {email}")
        response = requests.post(f"{USERS_API_URL}/api/v1/users/auth", json={"email": email, "password": password})
        logger.debug(f"Response received from API: {response.json()}")
        return response.json(), response.status_code

    def get_user_info(self, token):
        """
        Get user information.
        :param token: User's token.
        :return: User information.
        """
        logger.debug(f"Getting user info with token: {token}")
        headers = {'Authorization':  token}
        response = requests.get(f"{USERS_API_URL}/api/v1/users/me", headers=headers)
        logger.debug(f"Response received from API: {response.json()}")
        return response.json(), response.status_code
