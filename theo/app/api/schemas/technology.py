from typing import List
from .item import Item

from pydantic import BaseModel


class TechnologyBase(BaseModel):
    title: str | None = None
    description: str | None = None


class TechnologyCreate(TechnologyBase):
    pass


class TechnologyUpdate(TechnologyBase):
    pass


class TechnologyInDBBase(TechnologyBase):
    id: int
    title: str
    description: str
    items: List[Item]

    class Config:
        orm_mode = True


class Technology(TechnologyInDBBase):
    pass


class TechnologyInDB(TechnologyInDBBase):
    pass
