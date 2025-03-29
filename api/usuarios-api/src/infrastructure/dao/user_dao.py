from ..database.declarative_base import Session
from ..model.user_model import UserModel

class UserDAO:
    """
    Data Access Object for User.
    """

    @classmethod
    def save(cls, user: UserModel) -> str:
        session = Session()
        session.add(user)
        session.commit()
        session.refresh(user)
        session.close()
        return user.id

    @classmethod
    def find_by_email(cls, email: str) -> UserModel | None:
        """
        Find a user by email.
        :param email: Email of the user to find.
        :return: UserModel if found, None otherwise.
        """
        session = Session()
        user = session.query(UserModel).filter(UserModel.email == email).first()
        session.close()
        return user

