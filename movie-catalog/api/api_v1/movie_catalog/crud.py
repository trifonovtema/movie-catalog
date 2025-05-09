import logging

from pydantic import BaseModel, ValidationError
from redis import Redis

from core import config
from core.config import MOVIE_STORAGE_FILEPATH
from schemas.movie import (
    Movie,
    MovieUpdate,
    MovieUpdatePartial,
)

logger = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_MOVIE_CATALOG_DB,
    decode_responses=True,
)


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}
    # file_name: str = MOVIE_STORAGE_FILEPATH

    @classmethod
    def from_state(cls) -> "MovieStorage":
        if not MOVIE_STORAGE_FILEPATH.exists():
            return MovieStorage()
        return cls.model_validate_json(MOVIE_STORAGE_FILEPATH.read_text())

    def save_state(self) -> None:
        MOVIE_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        logger.info("Storage saved on disk")

    # def save_to_disk(self):
    #     with open(self.file_name, "w") as f:
    #         for movie in self.slug_to_movie.values():
    #             f.write(movie.model_dump_json())
    #             f.write("\n")
    #
    # def load_from_disk(self):
    #     try:
    #         with open(self.file_name, "r") as f:
    #             for line in f:
    #                 try:
    #                     movie = Movie.model_validate_json(line)
    #                     self.slug_to_movie[movie.slug] = movie
    #                 except ValueError as e:
    #                     print(f"Invalid movie: {line}. Error: {e}")
    #     except FileNotFoundError:
    #         self.create_storage()

    # def create_storage(self):
    #     with open(self.file_name, "w") as f:
    #         f.write("")

    def get(self) -> list[Movie] | None:
        return [
            Movie.model_validate_json(movie)
            for movie in redis.hvals(name=config.REDIS_MOVIE_CATALOG_HASH_NAME)
        ]

    def get_by_slug(self, slug: str) -> Movie | None:
        if res := redis.hget(
            name=config.REDIS_MOVIE_CATALOG_HASH_NAME,
            key=slug,
        ):
            return Movie.model_validate_json(res)
        return None

    def create(self, movie: Movie) -> Movie:
        self.save_to_storage(movie)
        logger.info("Movie %s created", movie.slug)
        return movie

    @classmethod
    def save_to_storage(cls, movie) -> int:
        return redis.hset(
            name=config.REDIS_MOVIE_CATALOG_HASH_NAME,
            key=movie.slug,
            value=movie.model_dump_json(),
        )

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)
        # self.save_to_disk()
        # self.save_state()

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)
        # self.save_to_disk()
        # self.save_state()

    def update(self, movie: Movie, movie_in: MovieUpdate) -> Movie:
        for field, value in movie_in:
            setattr(movie, field, value)
        self.save_to_storage(movie)
        return movie

    def update_partial(self, movie: Movie, movie_in: MovieUpdatePartial) -> Movie:
        for field, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field, value)
        self.save_to_storage(movie)
        return movie

    def init_storage(self):
        try:
            data = self.from_state()
        except ValidationError as e:
            logger.warning("Error loading storage: %s", e)
            self.save_state()
            logger.warning("Storage recreated")
            return

        self.slug_to_movie.update(
            data.slug_to_movie,
        )
        logger.warning("Storage loaded from disk")


storage = MovieStorage()
