# src/infrastructure/config/container.py
import os

from ..adapters.token_validator_adapter import TokenValidatorAdapter
from ...domain.ports.token_validator import TokenValidatorPort


class DependencyContainer:
    """Container for application dependencies"""

    def __init__(self):
        # Configure the token validator with the users API URL from environment
        users_api_url = os.getenv("USERS_API_URL", "http://users-api:5000")
        self._token_validator = TokenValidatorAdapter(users_api_url)

    @property
    def token_validator(self) -> TokenValidatorPort:
        return self._token_validator