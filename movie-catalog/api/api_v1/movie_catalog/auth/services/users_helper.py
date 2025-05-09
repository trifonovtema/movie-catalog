from abc import ABC, abstractmethod


class AbstractUsersHelper(ABC):
    @abstractmethod
    def get_user_password(self, user: str) -> str | None:
        """
        Get user password by username.
        Return password or None
        :param user:
        :return:
        """

    @classmethod
    def check_passwords_match(cls, password1: str, password2: str) -> bool:
        return password1 == password2

    def validate_user_password(self, user: str, password: str) -> bool:
        """
        Check if a user password is valid
        :param user:
        :param password:
        :return:
        """

        db_password = self.get_user_password(user)
        if db_password is None:
            return False
        return self.check_passwords_match(db_password, password)
