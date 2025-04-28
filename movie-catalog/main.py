from typing import Annotated

import uvicorn
from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    status,
    Depends,
)

from schemas.movie import Movie

app = FastAPI(
    title="Movie Catalog",
)

MOVIES = [
    Movie(
        id=1,
        name="One",
        description="Movie One",
        year=2021,
    ),
    Movie(
        id=2,
        name="Two",
        description="Movie Two",
        year=2022,
    ),
    Movie(
        id=3,
        name="Three",
        description="Movie Three",
        year=2023,
    ),
    Movie(
        id=4,
        name="Four",
        description="Movie Four",
        year=2024,
    ),
]


@app.get("/")
async def root(
    request: Request,
):
    docs_url = request.url.replace(path="/docs")
    return {
        "message": "This is the root of the movie catalog API",
        "docs": str(docs_url),
    }


@app.get(
    "/movies/",
    response_model=list[Movie],
)
@app.get(
    "/movies",
    response_model=list[Movie],
)
async def get_all_movies():
    return MOVIES


def prefetch_movie_by_id(
    movie_id: int,
) -> Movie:
    movie: Movie | None = next(filter(lambda m: m.id == movie_id, MOVIES), None)
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with id {movie_id!r} not found",
    )


@app.get(
    "/movies/{movie_id}",
    response_model=Movie,
)
@app.get(
    "/movies/{movie_id}/",
    response_model=Movie,
)
async def get_movie_by_id(
    movie: Annotated[
        Movie,
        Depends(prefetch_movie_by_id),
    ],
):
    return movie
