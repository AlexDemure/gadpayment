import decimal
import typing

from pydantic import BaseModel
from pydantic import HttpUrl

from src.domain.collections import PaymentCurrency
from src.domain.models import Payment as _Payment


class CreatePayment(BaseModel):
    amount: decimal.Decimal
    currency: PaymentCurrency
    webhook_url: HttpUrl
    description: str | None = None
    context: _Payment.PaymentContext

    def deserialize(self) -> dict[str, typing.Any]:
        data = self.model_dump()
        data["webhook_url"] = str(data["webhook_url"])
        data["context"] = self.context.model_dump()
        return data


class Payment(_Payment):
    @classmethod
    def serialize(cls, payment: _Payment) -> typing.Self:
        return cls.model_validate(payment)
