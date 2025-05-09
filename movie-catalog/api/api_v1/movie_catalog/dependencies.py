import logging
from typing import Annotated

from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
    status,
)
from fastapi.params import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    HTTPBasicCredentials,
    HTTPBasic,
)

from api.api_v1.movie_catalog.auth.services.redis_users_helper import redis_users
from api.api_v1.movie_catalog.crud import storage
from api.api_v1.movie_catalog.auth.services.redis_tokens_helper import redis_tokens
from schemas.movie import Movie

logger = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "DELETE",
        "PUT",
        "PATCH",
    },
)

static_api_token = HTTPBearer(
    scheme_name="api-token",
    description="API Token",
    auto_error=False,
)

basic_auth_token = HTTPBasic(
    scheme_name="Basic",
    description="Basic Auth",
    auto_error=False,
)


def prefetch_movie_by_slug(
    slug: str,
) -> Movie:
    movie: Movie | None = storage.get_by_slug(slug)
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with slug {slug!r} not found",
    )


def save_movie_storage_state(
    request: Request,
    background_tasks: BackgroundTasks,
):
    yield
    if request.method in UNSAFE_METHODS:
        background_tasks.add_task(storage.save_state)
        logger.info(f"Background task for save movie storage state added")


def api_token_check_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return
    validate_api_token(api_token)


def validate_api_token(api_token):
    if api_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized. Token is required.",
        )
    if redis_tokens.is_token_exists(api_token.credentials):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized. Invalid token",
    )


def user_basic_auth_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPBasicCredentials | None,
        Depends(basic_auth_token),
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return
    validate_user_auth(api_token)


def validate_user_auth(api_token: HTTPBasicCredentials):
    if api_token and redis_users.validate_user_password(
        user=api_token.username,
        password=api_token.password,
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized. Username or password is incorrect.",
        # headers={"WWW-Authenticate": "Basic"},
    )


def api_token_or_user_basic_auth_required_for_unsafe_methods(
    request: Request,
    user_credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(basic_auth_token),
    ] = None,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
) -> None:
    if request.method not in UNSAFE_METHODS:
        return
    if api_token:
        validate_api_token(api_token)
        return
    if user_credentials:
        validate_user_auth(user_credentials)
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized. Username and password or API token must be specified.",
    )
