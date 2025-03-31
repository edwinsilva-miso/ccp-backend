from ..model.user_model import UserModel
from ...domain.entities.user_dto import UserDTO


class UserMapper:

    @staticmethod
    def to_domain(user_dto: UserDTO) -> UserModel | None:
        """
        Converts a UserDTO to a UserModel.
        :param user_dto:
        :return:
        """
        if user_dto is None:
            return None

        return UserModel(
            id=user_dto.id,
            name=user_dto.name,
            phone=user_dto.phone,
            email=user_dto.email,
            password=user_dto.password,
            salt=user_dto.salt,
            role=user_dto.role
        )

    @staticmethod
    def to_dto(user: UserModel) -> UserDTO | None:
        """
        Converts a UserModel to a UserDTO.
        :param user:
        :return:
        """
        if user is None:
            return None

        return UserDTO(
            user.id,
            user.name,
            user.phone,
            user.email,
            user.password,
            user.salt,
            user.role
        )

    @staticmethod
    def to_domain_list(users_dto: list[UserDTO]) -> list[UserModel]:
        """
        Converts a list of UserDTO to a list of UserModel.
        :param users_dto:
        :return:
        """
        return [UserMapper.to_domain(user) for user in users_dto]

    @staticmethod
    def to_dto_list(users: list[UserModel]) -> list[UserDTO]:
        """
        Converts a list of UserModel to a list of UserDTO.
        :param users:
        :return:
        """
        return [UserMapper.to_dto(user) for user in users]
