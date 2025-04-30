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


class MovieStorage:
    slug_to_movie: dict[str, Movie] = {}
    file_name: str = "movies_storage.json"

    def __init__(self):
        self.load_from_disk()

    def save_to_disk(self):
        with open(self.file_name, "w") as f:
            for movie in self.slug_to_movie.values():
                f.write(movie.model_dump_json())
                f.write("\n")

    def load_from_disk(self):
        try:
            with open(self.file_name, "r") as f:
                for line in f:
                    try:
                        movie = Movie.model_validate_json(line)
                        self.slug_to_movie[movie.slug] = movie
                    except ValueError as e:
                        print(f"Invalid movie: {line}. Error: {e}")
        except FileNotFoundError:
            self.create_storage()

    def create_storage(self):
        with open(self.file_name, "w") as f:
            f.write("")

    def get(self):
        return self.slug_to_movie.values()

    def get_by_slug(self, slug: str):
        return self.slug_to_movie.get(slug)

    def create(self, movie: Movie):
        self.slug_to_movie[movie.slug] = movie
        self.save_to_disk()

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)
        self.save_to_disk()

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)
        self.save_to_disk()

    def update(self, movie: Movie, movie_in: MovieUpdate) -> Movie:
        for field, value in movie_in:
            setattr(movie, field, value)
        self.save_to_disk()
        return movie

    def update_partial(self, movie: Movie, movie_in: MovieUpdatePartial) -> Movie:
        for field, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field, value)
        self.save_to_disk()
        return movie


storage = MovieStorage()


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
