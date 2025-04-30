from pydantic import BaseModel


class MovieBase(BaseModel):
    name: str
    description: str
    year: int


class Movie(MovieBase):
    slug: str


class MovieUpdate(MovieBase):
    pass


class MovieCreate(MovieBase):
    slug: str
