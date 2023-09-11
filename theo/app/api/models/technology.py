from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base_class import Base

if TYPE_CHECKING:
    from .item import Item


class Technology(Base):
    __tablename__ = "technology"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(nullable=True)

    items: Mapped[List["Item"]] = relationship(cascade="all, delete-orphan")
