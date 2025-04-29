from schemas.movie import Movie

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
