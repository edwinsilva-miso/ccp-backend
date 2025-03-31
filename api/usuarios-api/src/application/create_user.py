import logging
import re

from .errors.errors import InvalidFormatError, UserAlreadyExistsError
from ..domain.entities.user_dto import UserDTO
from ..domain.utils import constants
from ..domain.utils.security_utils import SecurityUtils

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class CreateUser:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, user: UserDTO) -> str:
        """
        Create a new user in the system.
        :param user: Instance of UserDTO containing user information.
        :return: a str with the ID of the created user.
        """
        logging.debug(f"Creating user: {user.__str__()}")

        logging.debug("Validating user information...")
        email_pattern = constants.EMAIL_PATTERN
        password_pattern = constants.PASSWORD_PATTERN

        if not re.match(email_pattern, user.email) or not re.match(password_pattern, user.password):
            logging.error("Invalid email or password format.")
            raise InvalidFormatError

        logging.debug(f"Checking if user {user.email} already exists...")
        existing_user = self.user_repository.find_by_email(user.email)
        if existing_user:
            logging.error(f"User {user.email} already exists.")
            raise UserAlreadyExistsError

        utils = SecurityUtils()
        salt, hashed_password = utils.hash_password(user.password)

        user.password = hashed_password
        user.salt = salt

        return self.user_repository.add(user)
