from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base_class import Base

if TYPE_CHECKING:
    from .cribbly import Cribbly
    from .boom import Boom


class Crabble(Base):
    __tablename__ = "crabble"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    body: Mapped[str] = mapped_column(nullable=True)
    image: Mapped[str] = mapped_column(nullable=True)
    owner_id: Mapped[int] = mapped_column(index=True)

    cribbly_id: Mapped[int] = mapped_column(ForeignKey("cribbly.id"), index=True)
    cribbly: Mapped["Cribbly"] = relationship(back_populates="crabbles")

    booms: Mapped[List["Boom"]] = relationship(cascade="all, delete-orphan")
