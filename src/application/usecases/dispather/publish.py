import datetime

from src.decorators import sessionmaker
from src.infrastructure.brokers.rabbitmq import rabbit
from src.infrastructure.brokers.rabbitmq.collections import Topic
from src.infrastructure.brokers.rabbitmq.commands import PaymentNew
from src.infrastructure.databases.orm.sqlalchemy.queries import Filter
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.postgres import adapters


class Repository:
    def __init__(self, session: Session) -> None:
        self.outbox = adapters.repositories.Outbox(session)


class Broker:
    def __init__(self) -> None:
        self.rabbit = rabbit


class Container:
    def __init__(self, repository: Repository, broker: Broker) -> None:
        self.repository = repository
        self.broker = broker


class Usecase:
    def __init__(self) -> None:
        self.container: Container | None = None

    def build(self, session: Session) -> None:
        self.container = Container(repository=Repository(session), broker=Broker())

    @sessionmaker.write
    async def execute(self, session: Session) -> None:
        self.build(session)

        events = await self.container.repository.outbox.all(Filter.is_(key="published", value=None))

        for event in events:
            if Topic(event.topic) is Topic.payment_new:
                command = PaymentNew(
                    event_id=str(event.id),
                    payment_id=event.payload["payment_id"],
                )
            else:
                raise NotImplementedError()

            await self.container.broker.rabbit.publish(command.model_dump(mode="json"), queue=event.topic)

            await self.container.repository.outbox.update(
                id=str(event.id),
                published=datetime.datetime.now(datetime.UTC),
            )
