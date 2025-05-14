from redis import Redis

from api.api_v1.movie_catalog.auth.services.tokens_helper import AbstractTokensHelper
from core import config
from core.config import REDIS_API_TOKENS_SET_NAME


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

    def get_tokens(self) -> list[str]:
        return list(
            self.redis.smembers(
                name=self.token_set_name,
            )
        )


redis_tokens = RedisTokensHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_TOKENS_DB,
)
