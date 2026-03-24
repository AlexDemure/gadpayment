import datetime
import typing

from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.infrastructure.databases.orm.sqlalchemy.tables import Base
from src.infrastructure.databases.postgres.collections.const.column import LENGTH_MIDDLE_STR


class Outbox(Base):
    __tablename__ = "outbox"

    id: Mapped[str] = mapped_column(String(LENGTH_MIDDLE_STR), primary_key=True)
    topic: Mapped[str] = mapped_column(String(LENGTH_MIDDLE_STR), nullable=False)
    errors: Mapped[int] = mapped_column(Integer, nullable=False)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    published: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    accepted: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    failed: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    completed: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    payload: Mapped[dict[str, typing.Any]] = mapped_column(JSONB, nullable=False)
