import logging

from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
)
from starlette import status

from api.api_v1.movie_catalog.crud import storage
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
