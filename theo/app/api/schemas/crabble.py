from pydantic import BaseModel
from typing import List
from .boom import Boom


class CrabbleBase(BaseModel):
    name: str | None = None
    body: str | None = None
    image: str | None = None


class CrabbleCreate(CrabbleBase):
    pass


class CrabbleUpdate(CrabbleBase):
    pass


class CrabbleInDBBase(CrabbleBase):
    id: int
    name: str
    body: str
    image: str
    cribbly_id: int
    owner_id: int
    booms: List[Boom] | None

    class Config:
        orm_mode = True


class Crabble(CrabbleInDBBase):
    pass


class CrabbleInDB(CrabbleInDBBase):
    pass
