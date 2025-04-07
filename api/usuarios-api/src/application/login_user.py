import logging

from .errors.errors import UserNotExistsError


logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

class LoginUser:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, email, password) -> dict[str, str] | None:
        """
        Authenticate a user by checking the provided email and password.
        :param email: email of the user.
        :param password: password of the user.
        :return: Dictionary with token and user information if authentication is successful, None otherwise.
        """
        logging.debug(f"Authenticating user with email: {email}")

        logging.debug("Validating id user exists...")
        authenticated_user = self.user_repository.find_by_email(email)
        if not authenticated_user:
            logging.error(f"User with email {email} not found.")
            raise UserNotExistsError

        logging.debug("Checking password with found user...")
        if not authenticated_user.check_password(password):
            logging.error(f"Password does not match for user {email}.")
            raise UserNotExistsError

        logging.debug("Generating token...")
        authenticated_user.generate_token()

        logging.debug("Refresh user information...")
        self.user_repository.update(authenticated_user)

        return {
            'id': authenticated_user.id,
            'token': authenticated_user.token,
            'expiresAt': authenticated_user.expired_at
        }
