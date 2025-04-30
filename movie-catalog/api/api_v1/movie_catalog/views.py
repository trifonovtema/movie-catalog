import random
from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
    status,
    Form,
)

from api.api_v1.movie_catalog.crud import storage
from api.api_v1.movie_catalog.dependencies import prefetch_movie_by_slug
from schemas.movie import (
    Movie,
    MovieCreate,
)

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get(
    "/",
    response_model=list[Movie],
)
async def get_all_movies():
    return storage.get()


@router.post(
    "/form",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
async def add_movie_from_form(
    slug: Annotated[str, Form()],
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    year: Annotated[int, Form()],
):
    movie = Movie(
        slug=slug,
        name=name,
        description=description,
        year=year,
    )
    storage.create(movie)
    return movie


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
async def add_movie(
    movie: MovieCreate,
):
    storage.create(
        Movie(
            **movie.model_dump(),
        )
    )

    return Movie(
        **movie.model_dump(),
    )


@router.get(
    "/{slug}",
    response_model=Movie,
    status_code=status.HTTP_200_OK,
)
@router.get(
    "/{slug}/",
    response_model=Movie,
)
async def get_movie_by_slug(
    movie: Annotated[
        Movie,
        Depends(prefetch_movie_by_slug),
    ],
):
    return movie


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
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
async def delete_movie_by_slug(
    movie: Annotated[
        Movie,
        Depends(prefetch_movie_by_slug),
    ],
):
    storage.delete(movie)
