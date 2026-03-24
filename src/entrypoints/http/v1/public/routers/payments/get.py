from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi import status

from src.application.usecases.payments.get import Usecase
from src.entrypoints.http.common.deps import api_key
from src.entrypoints.http.v1.public.deps.payments.get import dependency
from src.entrypoints.http.v1.public.schemas import Payment


router = APIRouter()


@router.get(
    "/payments/{payment_id}",
    status_code=status.HTTP_200_OK,
    response_model=Payment,
    dependencies=[Depends(api_key)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_404_NOT_FOUND: {},
    },
)
async def query(
    payment_id: str = Path(...),
    usecase: Usecase = Depends(dependency),
) -> Payment:
    model = await usecase.execute(payment_id=payment_id)
    return Payment.serialize(model)
