from fastapi import APIRouter, status

from api.dependencies import WalletServiceDep
from schemas.wallet import WalletRead

router = APIRouter(prefix="/wallets", tags=["Wallets"])


@router.post(
    "",
    response_model=WalletRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_wallet(
    service: WalletServiceDep,
) -> WalletRead:
    wallet = await service.create_wallet()

    return WalletRead.model_validate(wallet)