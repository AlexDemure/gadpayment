import datetime
import typing
import uuid

from .base import Base


class Event(Base):
    id: uuid.UUID
    topic: str
    errors: int
    created: datetime.datetime
    updated: datetime.datetime
    published: datetime.datetime | None
    accepted: datetime.datetime | None
    failed: datetime.datetime | None
    completed: datetime.datetime | None
    payload: dict[str, typing.Any]

    @classmethod
    def init(cls, topic: str, payload: dict[str, typing.Any]) -> dict[str, typing.Any]:
        return dict(
            id=str(uuid.uuid4()),
            topic=topic,
            errors=0,
            created=datetime.datetime.now(datetime.UTC),
            updated=datetime.datetime.now(datetime.UTC),
            published=None,
            accepted=None,
            failed=None,
            completed=None,
            payload=payload,
        )
