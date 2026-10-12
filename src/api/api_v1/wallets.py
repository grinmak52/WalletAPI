from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import WalletServiceDep
from src.core.exceptions import InsufficientFundsError, WalletNotFoundError
from src.schemas.wallet import WalletOperation, WalletRead

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


@router.get(
    "/{wallet_uuid}",
    response_model=WalletRead,
    status_code=status.HTTP_200_OK,
)
async def get_wallet(
    wallet_uuid: UUID,
    service: WalletServiceDep,
) -> WalletRead:
    try:
        wallet = await service.get_wallet(wallet_uuid)
    except WalletNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found",
        ) from exc

    return WalletRead.model_validate(wallet)


@router.post(
    "/{wallet_uuid}/operation",
    response_model=WalletRead,
    status_code=status.HTTP_200_OK,
)
async def wallet_operation(
    wallet_uuid: UUID,
    operation: WalletOperation,
    service: WalletServiceDep,
) -> WalletRead:
    try:
        wallet = await service.apply_operation(
            wallet_id=wallet_uuid,
            amount=operation.amount,
            operation_type=operation.operation_type.value,
        )
    except WalletNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found",
        ) from exc
    except InsufficientFundsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Insufficient funds",
        ) from exc

    return WalletRead.model_validate(wallet)
