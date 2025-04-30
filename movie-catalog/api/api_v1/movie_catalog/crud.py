from pydantic import BaseModel, ValidationError

from core.config import MOVIE_STORAGE_FILEPATH
from schemas.movie import (
    Movie,
    MovieUpdate,
    MovieUpdatePartial,
)

MOVIES = [
    Movie(
        slug="one",
        name="One",
        description="Movie One",
        year=2021,
        notes="",
    ),
    Movie(
        slug="two",
        name="Two",
        description="Movie Two",
        year=2022,
        notes="",
    ),
    Movie(
        slug="three",
        name="Three",
        description="Movie Three",
        year=2023,
        notes="",
    ),
    Movie(
        slug="four",
        name="Four",
        description="Movie Four",
        year=2024,
        notes="",
    ),
]


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

    def get(self):
        return self.slug_to_movie.values()

    def get_by_slug(self, slug: str):
        return self.slug_to_movie.get(slug)

    def create(self, movie: Movie):
        self.slug_to_movie[movie.slug] = movie
        # self.save_to_disk()
        self.save_state()

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)
        # self.save_to_disk()
        self.save_state()

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)
        # self.save_to_disk()
        self.save_state()

    def update(self, movie: Movie, movie_in: MovieUpdate) -> Movie:
        for field, value in movie_in:
            setattr(movie, field, value)
        # self.save_to_disk()
        self.save_state()
        return movie

    def update_partial(self, movie: Movie, movie_in: MovieUpdatePartial) -> Movie:
        for field, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field, value)
        # self.save_to_disk()
        self.save_state()
        return movie


try:
    storage = MovieStorage.from_state()
except ValidationError as e:
    print(f"Error loading storage: {e}")
    storage = MovieStorage()
    storage.save_state()

# storage.create(
#     Movie(
#         slug="one",
#         name="One",
#         description="Movie One",
#         year=2021,
#         notes="",
#     )
# )
#
# storage.create(
#     Movie(
#         slug="two",
#         name="Two",
#         description="Movie Two",
#         year=2022,
#         notes="",
#     )
# )
#
# storage.create(
#     Movie(
#         slug="three",
#         name="Three",
#         description="Movie Three",
#         year=2023,
#         notes="",
#     )
# )
#
# storage.create(
#     Movie(
#         slug="four",
#         name="Four",
#         description="Movie Four",
#         year=2024,
#         notes="",
#     )
# )
