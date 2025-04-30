from typing import Annotated

from fastapi import APIRouter, Form
from starlette import status

from api.api_v1.movie_catalog.crud import storage
from schemas.movie import Movie, MovieCreate, MovieRead

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get(
    "/",
    response_model=list[MovieRead],
)
async def get_all_movies() -> list[Movie]:
    return storage.get()


@router.post(
    "/form",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_movie_from_form(
    slug: Annotated[str, Form()],
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    year: Annotated[int, Form()],
) -> Movie:
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
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_movie(
    movie: MovieCreate,
) -> Movie:
    return storage.create(
        Movie(
            **movie.model_dump(),
        )
    )