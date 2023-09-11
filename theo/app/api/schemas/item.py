from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    body: str | None = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemInDBBase(ItemBase):
    id: int
    name: str
    body: str
    technology_id: int

    class Config:
        orm_mode = True


class Item(ItemInDBBase):
    pass


class ItemInDB(ItemInDBBase):
    pass
