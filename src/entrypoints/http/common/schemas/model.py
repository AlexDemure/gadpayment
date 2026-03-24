import typing
import uuid

from pydantic import BaseModel

from src.domain.models import Model


class ID(BaseModel):
    id: int | str | uuid.UUID

    @classmethod
    def serialize(cls, model: Model) -> typing.Self:
        if not hasattr(model, "id"):
            raise ValueError
        return cls(id=model.id)
