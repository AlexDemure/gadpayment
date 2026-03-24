import enum


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    succeeded = "succeeded"
    failed = "failed"


class PaymentCurrency(str, enum.Enum):
    rub = "RUB"
    usd = "USD"
    eur = "EUR"
