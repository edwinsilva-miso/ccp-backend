from abc import ABC, abstractmethod
from ..entities.user_dto import UserDTO

class UserDTORepository(ABC):

    @abstractmethod
    def add(self, user: UserDTO) -> str:
        """
        Add a new user to the repository.
        :param user: UserDTO to add.
        :return: ID of the added user.
        """
        pass

    @abstractmethod
    def update(self, user: UserDTO) -> None:
        """
        Update a user in the repository.
        :param user: UserDTO to update.
        """
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> UserDTO | None:
        """
        Find a user by email.
        :param email: Email of the user to find.
        :return: UserDTO if found, None otherwise.
        """
        pass