import asyncio
import datetime
import logging
import random

import httpx

from src.configuration import settings
from src.decorators import sessionmaker
from src.domain.collections import PaymentStatus
from src.infrastructure.brokers.rabbitmq.commands import PaymentNew
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
    async def execute(self, session: Session, command: PaymentNew) -> None:
        async def fake_process() -> PaymentStatus:
            await asyncio.sleep(random.randint(2, 5))  # 2-5 сек
            return PaymentStatus.succeeded if random.random() < 0.9 else PaymentStatus.failed  # 90% успех, 10% ошибка

        self.build(session)

        event = await self.container.repository.outbox.one(Filter.eq(key="id", value=command.event_id))

        await self.container.repository.outbox.update(
            id=command.event_id,
            accepted=datetime.datetime.now(datetime.UTC),
        )

        try:
            payment = await self.container.repository.payment.one(Filter.eq(key="id", value=command.payment_id))

            status = await fake_process()

            if settings.WEBHOOK:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(
                        url=payment.webhook_url,
                        json={
                            "payment_id": str(payment.id),
                            "status": status.value,
                        },
                    )
                    response.raise_for_status()

            await self.container.repository.payment.update(
                id=command.payment_id,
                status=status,
                processed=datetime.datetime.now(datetime.UTC),
            )

            await self.container.repository.outbox.update(
                id=command.event_id,
                completed=datetime.datetime.now(datetime.UTC),
            )
        except Exception as e:
            logging.info(str(e))

            failed = datetime.datetime.now(datetime.UTC)

            if event.errors < 3:
                await self.container.repository.outbox.update(
                    id=command.event_id,
                    errors=event.errors + 1,
                    failed=failed,
                    published=None,
                )
            else:
                await self.container.repository.outbox.update(
                    id=command.event_id,
                    errors=event.errors + 1,
                    failed=failed,
                )
                await self.container.repository.payment.update(
                    id=command.payment_id,
                    status=PaymentStatus.failed.value,
                    processed=failed,
                )
