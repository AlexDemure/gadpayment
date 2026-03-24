import datetime
import typing

from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.infrastructure.databases.orm.sqlalchemy.tables import Base
from src.infrastructure.databases.postgres.collections.const.column import LENGTH_MIDDLE_STR
from src.infrastructure.databases.postgres.collections.const.column import LENGTH_TEXT


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(String(LENGTH_MIDDLE_STR), primary_key=True)
    amount: Mapped[str] = mapped_column(String(LENGTH_MIDDLE_STR), nullable=False)
    currency: Mapped[str] = mapped_column(String(LENGTH_MIDDLE_STR), nullable=False)
    description: Mapped[str | None] = mapped_column(String(LENGTH_TEXT), nullable=True)
    status: Mapped[str] = mapped_column(String(LENGTH_MIDDLE_STR), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(LENGTH_MIDDLE_STR), nullable=False, unique=True)
    webhook_url: Mapped[str] = mapped_column(String(LENGTH_MIDDLE_STR), nullable=False)
    processed: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    context: Mapped[dict[str, typing.Any]] = mapped_column(JSONB, nullable=False)
