import random
from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
    status,
    Form,
)

from api.api_v1.movie_catalog.crud import MOVIES
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
    return MOVIES


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
    return Movie(
        slug=slug,
        name=name,
        description=description,
        year=year,
    )


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
async def add_movie(
    movie: MovieCreate,
):
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
