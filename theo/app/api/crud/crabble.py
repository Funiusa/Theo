from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List
from .base import CRUDBase
from app.api.models.crabble import Crabble
from app.api.schemas.crabble import CrabbleCreate, CrabbleUpdate


class CRUDPost(CRUDBase[Crabble, CrabbleCreate, CrabbleUpdate]):
    def create_with_cribbly(
        self, db: Session, *, obj_in: CrabbleCreate, cribbly_id: int, owner_id: int
    ) -> Crabble:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, cribbly_id=cribbly_id, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_cribbly(
        self, db: Session, *, cribbly_id: int, skip: int = 0, limit: int = 100
    ) -> List[Crabble]:
        stmt = (
            select(self.model)
            .filter_by(cribbly_id=cribbly_id)
            .offset(skip)
            .limit(limit)
        )
        return db.execute(statement=stmt).scalars().all()

    def get_by_cribbly_id(self, db: Session, *, cribbly_id: int) -> Crabble:
        stmt = select(self.model).filter_by(cribbly_id=cribbly_id)
        return db.execute(statement=stmt).scalars().first()

    def retrieve_crabble_by_cribbly(self, db: Session, *, cribbly_id: int) -> Crabble:
        stmt = (
            select(self.model)
            .filter_by(cribbly_id=cribbly_id)
            .order_by(self.model.id.desc())
        )
        return db.execute(statement=stmt).scalars().first()


crabble = CRUDPost(Crabble)
