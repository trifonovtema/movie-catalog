import random
from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
    status,
    Form,
)
from starlette.requests import Request

from api.api_v1.movie_catalog.crud import MOVIES
from api.api_v1.movie_catalog.dependencies import prefetch_movie_by_id
from schemas.movie import Movie

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
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    year: Annotated[int, Form()],
):
    movie_id = random.randint(0, 1000000)
    return Movie(
        id=movie_id,
        name=name,
        description=description,
        year=year,
    )


@router.get(
    "/{movie_id}",
    response_model=Movie,
)
@router.get(
    "/{movie_id}/",
    response_model=Movie,
)
async def get_movie_by_id(
    movie: Annotated[
        Movie,
        Depends(prefetch_movie_by_id),
    ],
):
    return movie
