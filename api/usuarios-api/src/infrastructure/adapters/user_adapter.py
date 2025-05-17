from ..dao.user_dao import UserDAO
from ..mapper.user_mapper import UserMapper
from ...domain.entities.user_dto import UserDTO
from ...domain.repositories.user_repository import UserDTORepository


class UserAdapter(UserDTORepository):
    """
    Adapter for UserDTORepository to interact with UserDAO and UserMapper.
    """

    def add(self, user: UserDTO) -> str:
        """
        Adds a new user to the repository.
        """
        return UserDAO.save(UserMapper.to_domain(user))

    def update(self, user: UserDTO) -> None:
        """
        Update a user in the repository.
        :param user: UserDTO to update.
        """
        return UserDAO.update(UserMapper.to_domain(user))

    def find_by_email(self, email: str) -> UserDTO | None:
        """
        Find a user by email.
        :param email: Email of the user to find.
        :return: UserDTO if found, None otherwise.
        """
        user = UserDAO.find_by_email(email)
        return UserMapper.to_dto(user) if user else None

    def find_by_role(self, role: str) -> list[UserDTO]:
        """
        Find users by role.
        :param role: Role of the users to find.
        :return: List of UserDTOs with the specified role.
        """
        users = UserDAO.find_by_role(role)
        return [UserMapper.to_dto(user) for user in users]
