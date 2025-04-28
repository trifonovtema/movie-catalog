from pydantic import BaseModel


class Movie(BaseModel):
    id: int
    name: str
    description: str
    year: int
