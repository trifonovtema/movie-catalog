from schemas.movie import Movie, MovieUpdate, MovieUpdatePartial

MOVIES = [
    Movie(
        slug="one",
        name="One",
        description="Movie One",
        year=2021,
    ),
    Movie(
        slug="two",
        name="Two",
        description="Movie Two",
        year=2022,
    ),
    Movie(
        slug="three",
        name="Three",
        description="Movie Three",
        year=2023,
    ),
    Movie(
        slug="four",
        name="Four",
        description="Movie Four",
        year=2024,
    ),
]


class MovieStorage:
    slug_to_movie: dict[str, Movie] = {}

    def get(self):
        return self.slug_to_movie.values()

    def get_by_slug(self, slug: str):
        return self.slug_to_movie.get(slug)

    def create(self, movie: Movie):
        self.slug_to_movie[movie.slug] = movie

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)

    def update(self, movie: Movie, movie_in: MovieUpdate) -> Movie:
        for field, value in movie_in:
            setattr(movie, field, value)
        return movie

    def update_partial(self, movie: Movie, movie_in: MovieUpdatePartial) -> Movie:
        for field, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field, value)
        return movie


storage = MovieStorage()


storage.create(
    Movie(
        slug="one",
        name="One",
        description="Movie One",
        year=2021,
    )
)

storage.create(
    Movie(
        slug="two",
        name="Two",
        description="Movie Two",
        year=2022,
    )
)

storage.create(
    Movie(
        slug="three",
        name="Three",
        description="Movie Three",
        year=2023,
    )
)

storage.create(
    Movie(
        slug="four",
        name="Four",
        description="Movie Four",
        year=2024,
    )
)
