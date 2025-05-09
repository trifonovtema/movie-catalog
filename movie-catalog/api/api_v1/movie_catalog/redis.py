import secrets
from abc import ABC, abstractmethod

from redis import Redis

from core import config
from core.config import REDIS_API_TOKENS_SET_NAME


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

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(16)

    def generate_and_save_token(self, token: str) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token


class RedisTokensHelper(AbstractTokensHelper):
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
    ):
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )

        self.token_set_name = REDIS_API_TOKENS_SET_NAME

    def is_token_exists(self, token: str) -> bool:
        return bool(
            self.redis.sismember(
                name=self.token_set_name,
                value=token,
            )
        )

    def add_token(self, token: str) -> None:
        self.redis.sadd(
            self.token_set_name,
            token,
        )


redis_tokens = RedisTokensHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_TOKENS_DB,
)
