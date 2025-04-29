from pydantic import BaseModel


class MovieBase(BaseModel):
    slug: str
    name: str
    description: str
    year: int


class Movie(MovieBase):
    pass


class MovieCreate(MovieBase):
    pass
