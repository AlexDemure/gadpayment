import contextlib
import functools
import json
import typing

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from .collections import Isolation
from .encoders import JSONEncoder


class SQLAlchemy:
    def __init__(self, url: str) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url,
            echo=False,
            future=True,
            isolation_level=Isolation.read_committed,
            json_serializer=functools.partial(json.dumps, cls=JSONEncoder, ensure_ascii=False),
        )
        self.sessionmaker: async_sessionmaker[AsyncSession] = async_sessionmaker(self.engine, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def read(self) -> typing.AsyncGenerator[AsyncSession, None]:
        async with self.sessionmaker() as session:
            yield session

    @contextlib.asynccontextmanager
    async def write(self) -> typing.AsyncGenerator[AsyncSession, None]:
        async with self.sessionmaker() as session:
            async with session.begin():
                yield session
