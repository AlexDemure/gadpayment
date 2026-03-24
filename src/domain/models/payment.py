import datetime
import decimal
import typing
import uuid

from src.domain.collections import PaymentCurrency
from src.domain.collections import PaymentStatus

from .base import Base


class Payment(Base):
    class PaymentContext(Base): ...

    id: uuid.UUID
    amount: decimal.Decimal
    description: str | None
    currency: PaymentCurrency
    status: PaymentStatus
    idempotency_key: str
    webhook_url: str
    processed: datetime.datetime | None
    created: datetime.datetime
    updated: datetime.datetime
    context: PaymentContext

    @classmethod
    def init(
        cls,
        amount: decimal.Decimal,
        currency: PaymentCurrency,
        description: str | None,
        idempotency_key: str,
        webhook_url: str,
        context: PaymentContext,
    ) -> dict[str, typing.Any]:
        return dict(
            id=str(uuid.uuid4()),
            amount=str(amount),
            currency=currency,
            description=description,
            idempotency_key=idempotency_key,
            webhook_url=webhook_url,
            context=context,
            status=PaymentStatus.pending,
            processed=None,
            created=datetime.datetime.now(datetime.UTC),
            updated=datetime.datetime.now(datetime.UTC),
        )
