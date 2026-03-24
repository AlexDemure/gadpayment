from src.decorators import sessionmaker
from src.domain.models.payment import Payment
from src.infrastructure.databases.orm.sqlalchemy.queries import Filter
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.postgres import adapters


class Repository:
    def __init__(self, session: Session) -> None:
        self.payment = adapters.repositories.Payment(session)


class Container:
    def __init__(self, repository: Repository) -> None:
        self.repository = repository


class Usecase:
    def __init__(self) -> None:
        self.container: Container | None = None

    def build(self, session: Session) -> None:
        self.container = Container(repository=Repository(session))

    @sessionmaker.read
    async def execute(self, session: Session, payment_id: str) -> Payment:
        self.build(session)

        payment = await self.container.repository.payment.one(Filter.eq(key="id", value=payment_id))

        return payment
