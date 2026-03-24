import decimal
import typing

from src.decorators import sessionmaker
from src.domain.collections import PaymentAlreadyExists
from src.domain.collections import PaymentCurrency
from src.domain.models import Event
from src.domain.models import Payment
from src.infrastructure.brokers.rabbitmq.collections import Topic
from src.infrastructure.databases.orm.sqlalchemy.queries import Filter
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.postgres import adapters


class Repository:
    def __init__(self, session: Session) -> None:
        self.payment = adapters.repositories.Payment(session)
        self.outbox = adapters.repositories.Outbox(session)


class Container:
    def __init__(self, repository: Repository) -> None:
        self.repository = repository


class Usecase:
    def __init__(self) -> None:
        self.container: Container | None = None

    def build(self, session: Session) -> None:
        self.container = Container(repository=Repository(session))

    @sessionmaker.write
    async def execute(
        self,
        session: Session,
        amount: decimal.Decimal,
        currency: PaymentCurrency,
        description: str | None,
        idempotency_key: str,
        webhook_url: str,
        context: dict[str, typing.Any],
    ) -> Payment:
        self.build(session)

        if await self.container.repository.payment.exists(Filter.eq(key="idempotency_key", value=idempotency_key)):
            raise PaymentAlreadyExists

        payment = await self.container.repository.payment.create(
            model=Payment.init(
                amount=amount,
                currency=currency,
                description=description,
                idempotency_key=idempotency_key,
                webhook_url=webhook_url,
                context=Payment.PaymentContext.model_validate(context),
            )
        )

        await self.container.repository.outbox.create(
            model=Event.init(
                topic=Topic.payment_new,
                payload=dict(payment_id=payment.id),
            )
        )

        return payment
