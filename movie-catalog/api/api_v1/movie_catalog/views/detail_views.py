from typing import Annotated

from fastapi import Depends, APIRouter, BackgroundTasks
from starlette import status

from api.api_v1.movie_catalog.crud import storage
from api.api_v1.movie_catalog.dependencies import prefetch_movie_by_slug
from schemas.movie import Movie, MovieUpdate, MovieUpdatePartial, MovieRead

MovieBySlug = Annotated[
    Movie,
    Depends(prefetch_movie_by_slug),
]

router = APIRouter(
    prefix="/{slug}",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Movie deleted successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Movie not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie with slug 'slug' not found",
                    },
                },
            },
        },
    },
)


@router.get(
    "/",
    response_model=MovieRead,
)
async def get_movie_by_slug(
    movie: MovieBySlug,
) -> Movie:
    return movie


@router.put(
    path="/",
    status_code=status.HTTP_200_OK,
)
async def update_movie_by_slug(
    movie: MovieBySlug,
    movie_in: MovieUpdate,
    background_tasks: BackgroundTasks,
) -> Movie:
    background_tasks.add_task(storage.save_state)
    return storage.update(movie, movie_in)


@router.patch(
    path="/",
    status_code=status.HTTP_200_OK,
)
async def update_movie_by_slug(
    movie: MovieBySlug,
    movie_in: MovieUpdatePartial,
    background_tasks: BackgroundTasks,
) -> Movie:
    background_tasks.add_task(storage.save_state)
    return storage.update_partial(movie, movie_in)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_movie_by_slug(
    movie: MovieBySlug,
    background_tasks: BackgroundTasks,
) -> None:
    storage.delete(movie)
    background_tasks.add_task(storage.save_state)
