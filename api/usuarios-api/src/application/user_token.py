import logging

from .errors.errors import ForbiddenError, UserNotExistsError
from ..domain.utils.security_utils import SecurityUtils

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class UserToken:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, headers) -> dict[str, str]:
        """
        Get user information from the token.
        :param headers: Headers containing the requests.
        :return: Dictionary with user information.
        """
        logging.debug("Getting user information from token...")

        if not headers:
            logging.error("No headers provided.")
            raise ForbiddenError

        utils = SecurityUtils()
        payload = utils.decode_token(headers)

        logging.debug("Validating id user exists...")
        user = self.user_repository.find_by_email(payload['email'])
        if not user:
            logging.error("User not found.")
            raise UserNotExistsError

        return {
            'id': user.id,
            'name': user.name,
            'phone': user.phone,
            'email': user.email,
            'role': user.role.name
        }
