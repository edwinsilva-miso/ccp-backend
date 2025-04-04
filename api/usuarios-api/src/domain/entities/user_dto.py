import datetime

from ..utils.security_utils import SecurityUtils
from ...application.errors.errors import InvalidFormatError

class UserDTO:
    def __init__(self, id: str, name: str, phone: str, email: str, password: str, token: str, salt: str, role: str, expire_at: datetime):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.password = password
        self.token = token,
        self.salt = salt
        self.role = role
        self.expired_at = expire_at

    def __str__(self):
        return f'{self.id} - {self.name} - {self.phone} - {self.email} - {self.role}'

    def generate_password(self) -> dict[str, str | bytes]:
        """
        Generate a hashed password using the provided password.
        :param password: Password to hash.
        :return: Hashed password.
        """
        if self.password is None:
            raise InvalidFormatError

        utils = SecurityUtils()
        salt, hashed_password = utils.hash_password(self.password)
        return {
            'salt': salt,
            'hashed_password': hashed_password
        }

    def check_password(self, password: str) -> bool:
        """
        Check if the provided password matches the stored password.
        :param password: Password to check.
        :return: True if the password matches, False otherwise.
        """
        utils = SecurityUtils()
        return utils.verify_password(password, self.password)

    def generate_token(self) -> None:
        """
        Generate a JWT token for the user.
        :return: JWT token and expiration date.
        """
        utils = SecurityUtils()
        token, expire_at = utils.generate_token(self)
        self.token = token
        self.expired_at = expire_at
        # return {
        #     'token': token,
        #     'expire': expire_at
        # }
