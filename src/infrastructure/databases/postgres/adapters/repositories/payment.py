from src.domain import models
from src.domain.collections import exceptions
from src.infrastructure.databases.postgres import crud
from src.infrastructure.databases.postgres import tables

from .base import Base


class Payment(Base[crud.Payment, tables.Payment, models.Payment, exceptions.PaymentNotFound]):
    crud = crud.Payment
    table = tables.Payment
    model = models.Payment
    error = exceptions.PaymentNotFound
