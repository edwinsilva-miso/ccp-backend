import datetime

import bcrypt
import jwt
import pytz

from . import constants
from ...application.errors.errors import InvalidTokenError, ForbiddenError


class SecurityUtils:
    secret = constants.JWT_KEY
    tz = pytz.timezone(constants.DEFAULT_TIMEZONE)

    def hash_password(self, password: str) -> tuple[bytes, str]:
        """
        Hashes a password using SHA-256.

        :param password: The password to hash.
        :return: The hashed password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(constants.UTF_8_ENCODING), salt)
        return salt, hashed_password.decode(constants.UTF_8_ENCODING)

    def verify_password(self, password, hashed_password):
        """
        Verifies a password against a hashed password.
        :param password: The password to verify.
        :param hashed_password: The hashed password to verify against.
        :return: True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(password.encode(constants.UTF_8_ENCODING),
                              hashed_password.encode(constants.UTF_8_ENCODING))

    def generate_token(self, authenticated_user):
        """
        Generates a JWT token for the authenticated user.
        :param authenticated_user:
        :return:
        """
        now = datetime.datetime.now(tz=self.tz)
        exp_date = datetime.datetime.now(tz=self.tz) + datetime.timedelta(minutes=10)

        payload = {
            'iat': now,
            'exp': exp_date,
            'username': authenticated_user.username,
            'fullName': authenticated_user.full_name,
        }

        return jwt.encode(payload, self.secret, algorithm=constants.JWT_ALGORITHM), exp_date.isoformat()

    def decode_token(self, headers):
        """
        Decodes a JWT token from the headers.
        :param headers:
        :return:
        """
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]
            try:
                payload = jwt.decode(encoded_token, self.secret, algorithms=[constants.JWT_ALGORITHM])
                return payload
            except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError, jwt.DecodeError):
                raise InvalidTokenError
        else:
            raise ForbiddenError
