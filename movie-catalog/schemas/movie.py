from pydantic import BaseModel


class MovieBase(BaseModel):
    name: str
    description: str
    year: int


class Movie(MovieBase):
    id: int


class MovieCreate(MovieBase):
    pass
