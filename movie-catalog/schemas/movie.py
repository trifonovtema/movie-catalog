from pydantic import BaseModel


class MovieBase(BaseModel):
    name: str
    description: str
    year: int


class Movie(MovieBase):
    slug: str


class MovieUpdate(MovieBase):
    pass


class MovieUpdatePartial(MovieBase):
    name: str | None = None
    description: str | None = None
    year: int | None = None


class MovieCreate(MovieBase):
    slug: str
