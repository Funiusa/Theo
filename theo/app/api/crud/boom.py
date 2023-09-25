from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List
from .base import CRUDBase
from app.api.models.boom import Boom
from app.api.schemas.boom import BoomCreate, BoomUpdate


class CRUDPost(CRUDBase[Boom, BoomCreate, BoomUpdate]):
    def create_with_crabble(
        self, db: Session, *, obj_in: BoomCreate, crabble_id: int, owner_id: int
    ) -> Boom:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, crabble_id=crabble_id, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_crabble(
        self, db: Session, *, crabble_id: int, skip: int = 0, limit: int = 100
    ) -> List[Boom]:
        stmt = (
            select(self.model)
            .filter_by(crabble_id=crabble_id)
            .offset(skip)
            .limit(limit)
        )
        return db.execute(statement=stmt).scalars().all()

    def get_by_crabble_id(self, db: Session, *, crabble_id: int) -> Boom:
        stmt = select(self.model).filter_by(crabble_id=crabble_id)
        return db.execute(statement=stmt).scalars().first()

    def retrieve_boom_by_crabble(self, db: Session, *, crabble_id: int) -> Boom:
        stmt = (
            select(self.model)
            .filter_by(crabble_id=crabble_id)
            .order_by(self.model.id.desc())
        )
        return db.execute(statement=stmt).scalars().first()


boom = CRUDPost(Boom)
