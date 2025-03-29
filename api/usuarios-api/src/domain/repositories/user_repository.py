from abc import ABC, abstractmethod
from ..entities.user_dto import UserDTO

class UserDTORepository(ABC):

    @abstractmethod
    def add(self, user: UserDTO) -> str:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> UserDTO | None:
        """
        Find a user by email.
        :param email: Email of the user to find.
        :return: UserDTO if found, None otherwise.
        """
        pass