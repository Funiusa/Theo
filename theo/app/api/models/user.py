from __future__ import annotations
from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import BigInteger
from app.database.base_class import Base

if TYPE_CHECKING:
    from .cribbly import Cribbly


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(default=False, index=True)
    is_active: Mapped[bool] = mapped_column(default=True, index=True)

    cribblies: Mapped[List["Cribbly"]] = relationship(cascade="all, delete-orphan")
