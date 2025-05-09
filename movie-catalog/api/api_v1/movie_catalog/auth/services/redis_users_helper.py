from redis import Redis

from api.api_v1.movie_catalog.auth.services.tokens_helper import AbstractTokensHelper
from api.api_v1.movie_catalog.auth.services.users_helper import AbstractUsersHelper
from core import config
from core.config import REDIS_API_TOKENS_SET_NAME


class RedisUsersHelper(AbstractUsersHelper):
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

    def get_user_password(self, user: str) -> str | None:
        return self.redis.get(user)


redis_users = RedisUsersHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_USERS_DB,
)
