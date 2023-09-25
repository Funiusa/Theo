from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base_class import Base

if TYPE_CHECKING:
    from .user import User
    from .crabble import Crabble


class Cribbly(Base):
    __tablename__ = "cribbly"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False, index=True)
    description: Mapped[str] = mapped_column(nullable=True)
    image: Mapped[str] = mapped_column(nullable=True, default=None)

    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    owner: Mapped["User"] = relationship(back_populates="cribblies")

    crabbles: Mapped[List["Crabble"]] = relationship(cascade="all, delete-orphan")
