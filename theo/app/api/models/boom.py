from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base_class import Base

if TYPE_CHECKING:
    from .crabble import Crabble


class Boom(Base):
    __tablename__ = "boom"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    body: Mapped[str] = mapped_column(nullable=True)
    image: Mapped[str] = mapped_column(nullable=True, default=None)
    owner_id: Mapped[int] = mapped_column(index=True)

    crabble_id: Mapped[int] = mapped_column(ForeignKey("crabble.id"), index=True)
    crabble: Mapped["Crabble"] = relationship(back_populates="booms")
