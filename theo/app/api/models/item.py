from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base_class import Base

if TYPE_CHECKING:
    from .technology import Technology


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    body: Mapped[str] = mapped_column(nullable=True)

    technology_id: Mapped[int] = mapped_column(ForeignKey("technology.id"), index=True)
    technology: Mapped["Technology"] = relationship(back_populates="items")
