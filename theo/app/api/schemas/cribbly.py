from typing import List
from .crabble import Crabble

from pydantic import BaseModel


class CribblyBase(BaseModel):
    title: str | None = None
    description: str | None = None
    image: str | None = None


class CribblyCreate(CribblyBase):
    pass


class CribblyUpdate(CribblyBase):
    pass


class CribblyInDBBase(CribblyBase):
    id: int
    title: str
    description: str
    image: str
    owner_id: int
    crabbles: List[Crabble] | None = []

    class Config:
        orm_mode = True


class Cribbly(CribblyInDBBase):
    pass


class CribblyInDB(CribblyInDBBase):
    pass
