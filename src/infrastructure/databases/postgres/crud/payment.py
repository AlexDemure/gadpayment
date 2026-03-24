from src.infrastructure.databases.orm.sqlalchemy.crud import Base
from src.infrastructure.databases.postgres import tables


class Payment(Base[tables.Payment]):
    table = tables.Payment
