from fastapi import HTTPException
from starlette import status

from api.api_v1.movie_catalog.crud import MOVIES
from schemas.movie import Movie


def prefetch_movie_by_slug(
    slug: str,
) -> Movie:
    movie: Movie | None = next(filter(lambda m: m.slug == slug, MOVIES), None)
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with slug {slug!r} not found",
    )
