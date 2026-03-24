from fastapi import Depends
from faststream.rabbit import RabbitRouter

from src.application.usecases.payments.new import Usecase
from src.entrypoints.brokers.rabbitmq.subscribers.deps.payments.new import dependency
from src.infrastructure.brokers.rabbitmq.collections import Topic
from src.infrastructure.brokers.rabbitmq.commands import PaymentNew


router = RabbitRouter()


@router.subscriber(Topic.payment_new)
async def create(command: PaymentNew, usecase: Usecase = Depends(dependency)) -> None:
    await usecase.execute(command)
