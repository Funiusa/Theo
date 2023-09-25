from pydantic import BaseModel


class BoomBase(BaseModel):
    name: str | None = None
    body: str | None = None
    image: str | None = None


class BoomCreate(BoomBase):
    pass


class BoomUpdate(BoomBase):
    pass


class BoomInDBBase(BoomBase):
    id: int
    name: str
    body: str
    image: str
    owner_id: int
    crabble_id: int

    class Config:
        orm_mode = True


class Boom(BoomInDBBase):
    pass


class BoomInDB(BoomInDBBase):
    pass
