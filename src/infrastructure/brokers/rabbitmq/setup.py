from faststream.rabbit import RabbitBroker

from src.configuration import settings


rabbit = RabbitBroker(settings.RABBIT_HOST)
