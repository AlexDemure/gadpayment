from faststream.rabbit.fastapi import RabbitRouter

from src.configuration import settings

from . import subscribers


router = RabbitRouter(
    settings.RABBIT_HOST,
    schema_url="/asyncapi",
    include_in_schema=True,
)

router.include_router(subscribers.router, tags=["Subscriber"])
