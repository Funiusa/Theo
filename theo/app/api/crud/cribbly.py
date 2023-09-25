from typing import List
from .base import CRUDBase
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.api.models.cribbly import Cribbly
from app.api.schemas.cribbly import CribblyCreate, CribblyUpdate


class CRUDPost(CRUDBase[Cribbly, CribblyCreate, CribblyUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: CribblyCreate, owner_id: int
    ) -> Cribbly:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Cribbly]:
        stmt = select(self.model).filter_by(owner_id=owner_id).offset(skip).limit(limit)
        return db.execute(statement=stmt).scalars().all()


cribbly = CRUDPost(Cribbly)
