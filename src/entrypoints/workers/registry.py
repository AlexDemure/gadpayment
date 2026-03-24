from src.framework.background import background

from . import dispatcher


def workers() -> None:
    background.add(dispatcher.run)
