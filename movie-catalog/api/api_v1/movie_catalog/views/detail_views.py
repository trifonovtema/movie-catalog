from typing import Annotated

from fastapi import Depends, APIRouter
from starlette import status

from api.api_v1.movie_catalog.crud import storage
from api.api_v1.movie_catalog.dependencies import prefetch_movie_by_slug
from schemas.movie import Movie, MovieUpdate

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
    response_model=Movie,
)
async def get_movie_by_slug(
    movie: MovieBySlug,
):
    return movie


@router.put(
    path="/",
    status_code=status.HTTP_200_OK,
)
async def update_movie_by_slug(
    movie: MovieBySlug,
    movie_in: MovieUpdate,
):
    return storage.update(movie, movie_in)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_movie_by_slug(
    movie: MovieBySlug,
):
    storage.delete(movie)
