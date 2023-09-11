from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List
from .base import CRUDBase
from app.api.models.item import Item
from app.api.schemas.item import ItemCreate, ItemUpdate


class CRUDPost(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def create_with_technology(
            self, db: Session, *, obj_in: ItemCreate, technology_id: int
    ) -> Item:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, technology_id=technology_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_technology(
            self, db: Session, *, technology_id: int, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        stmt = (
            select(self.model).filter_by(
                technology_id=technology_id).offset(skip).limit(limit)
        )
        return db.execute(statement=stmt).scalars().all()

    def get_by_technology_id(self, db: Session, *, technology_id: int) -> Item:
        stmt = (
            select(self.model).filter_by(technology_id=technology_id))
        return db.execute(statement=stmt).scalars().first()

    def retrieve_item_by_technology(self, db: Session, *, technology_id: int) -> Item:
        stmt = (
            select(self.model)
            .filter_by(technology_id=technology_id)
            .order_by(self.model.id.desc())
        )
        return db.execute(statement=stmt).scalars().first()


item = CRUDPost(Item)
