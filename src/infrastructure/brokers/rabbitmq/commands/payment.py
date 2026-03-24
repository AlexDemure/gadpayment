from pydantic import BaseModel


class PaymentNew(BaseModel):
    event_id: str
    payment_id: str
