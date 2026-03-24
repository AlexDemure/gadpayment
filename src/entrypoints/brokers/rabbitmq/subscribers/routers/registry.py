from faststream.rabbit import RabbitRouter

from . import payments


router = RabbitRouter()

router.include_router(payments.router)
