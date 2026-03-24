import asyncio
import contextlib
import typing

from src.application.usecases.dispather.publish import Usecase
from src.infrastructure.brokers.rabbitmq import rabbit
from src.infrastructure.databases.postgres import postgres


@contextlib.asynccontextmanager
async def lifespan() -> typing.AsyncIterator[None]:
    postgres.start()
    await rabbit.start()
    yield
    await rabbit.stop()
    postgres.shutdown()


async def run(delay: float = 1.0) -> None:
    usecase = Usecase()
    async with lifespan():
        while True:
            await usecase.execute()
            await asyncio.sleep(delay)


if __name__ == "__main__":
    asyncio.run(run())
