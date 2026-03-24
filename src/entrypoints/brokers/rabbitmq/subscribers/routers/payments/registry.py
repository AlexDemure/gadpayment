from faststream.rabbit import RabbitRouter

from . import new


router = RabbitRouter()

router.include_router(new.router)
