from src.domain import models
from src.domain.collections import exceptions
from src.infrastructure.databases.postgres import crud
from src.infrastructure.databases.postgres import tables

from .base import Base


class Outbox(Base[crud.Outbox, tables.Outbox, models.Event, exceptions.EventNotFound]):
    crud = crud.Outbox
    table = tables.Outbox
    model = models.Event
    error = exceptions.EventNotFound
