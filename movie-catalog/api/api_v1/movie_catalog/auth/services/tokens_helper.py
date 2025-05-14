import secrets
from abc import ABC, abstractmethod


class AbstractTokensHelper(ABC):
    @abstractmethod
    def is_token_exists(cls, token: str) -> bool:
        """
        Check if a token is already exists
            :param token:
            :return:
        """

    @abstractmethod
    def add_token(self, token: str) -> None:
        """
        Add a token to storage
        :param token:
        :return:
        """

    @abstractmethod
    def get_tokens(self) -> list[str]:
        """
        Get all tokens
        :return:
        """

    @abstractmethod
    def delete_token(self, token: str) -> None:
        """
        Delete a token
        :param token:
        :return:
        """

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(16)

    def generate_and_save_token(self, token: str) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token
