import logging

from .errors.errors import ForbiddenError, UserNotExistsError

class FindUserByRole:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, role: str) -> list:
        """
        Find users by role.
        :param role: Role to search for.
        :return: List of users with the specified role.
        """
        logging.debug(f"Finding users with role: {role}")

        # Get all users with the specified role
        users = self.user_repository.find_by_role(role)

        # Transform users to dictionary for response
        users_response = []
        for user in users:
            users_response.append({
                'id': user.id,
                'name': user.name,
                'phone': user.phone,
                'email': user.email,
                'role': user.role.name
            })

        return users_response
