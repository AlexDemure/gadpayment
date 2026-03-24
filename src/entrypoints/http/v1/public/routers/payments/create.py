from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import status

from src.application.usecases.payments.create import Usecase
from src.entrypoints.http.common.deps import api_key
from src.entrypoints.http.common.deps import unique_key
from src.entrypoints.http.common.schemas import ID
from src.entrypoints.http.v1.public.deps.payments.create import dependency
from src.entrypoints.http.v1.public.schemas import CreatePayment


router = APIRouter()


@router.post(
    "/payments",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ID,
    dependencies=[Depends(api_key)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
    },
)
async def command(
    body: CreatePayment = Body(...),
    idempotency_key: str = Depends(unique_key),
    usecase: Usecase = Depends(dependency),
) -> ID:
    model = await usecase.execute(idempotency_key=idempotency_key, **body.deserialize())
    return ID.serialize(model)
