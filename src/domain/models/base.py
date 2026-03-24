import typing

from pydantic import BaseModel
from pydantic import ConfigDict


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="allow")

    @classmethod
    def init(cls, *args: typing.Any, **kwargs: typing.Any) -> typing.Self:
        raise NotImplementedError


Model = typing.TypeVar("Model", bound=Base)
