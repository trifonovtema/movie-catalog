import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MOVIE_STORAGE_FILEPATH = BASE_DIR / "movie_storage.json"

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


# API_TOKENS = frozenset(
#     {
#         "L7rg56lHJ4CF6bPK9pkOHg",
#         "dD9-iCLRDOutcmtr_xAFxw",
#     }
# )
#
# USER_DB: dict[str, str] = {
#     "user1": "password1",
#     "user2": "password2",
# }

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_TOKENS_DB = 1
REDIS_USERS_DB = 2
REDIS_MOVIE_CATALOG_DB = 3
REDIS_API_TOKENS_SET_NAME = "tokens"
REDIS_MOVIE_CATALOG_HASH_NAME = "movies"
