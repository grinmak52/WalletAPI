from decimal import Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import InsufficientFundsError, WalletNotFoundError
from src.models import Wallet
from src.repositories.wallet import WalletRepository
from src.schemas.wallet import OperationType


class WalletService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = WalletRepository(session)
        self.session = session

    async def create_wallet(self) -> Wallet:
        wallet = await self.repository.create()

        await self.session.commit()

        return wallet

    async def get_wallet(self, wallet_id: UUID) -> Wallet:
        wallet = await self.repository.get_by_id(wallet_id)

        if wallet is None:
            raise WalletNotFoundError(f"Wallet {wallet_id} not found")

        return wallet

    async def apply_operation(
        self,
        wallet_id: UUID,
        amount: Decimal,
        operation_type: OperationType,
    ) -> Wallet:
        wallet = await self.repository.apply_operation(
            wallet_id=wallet_id,
            amount=amount,
            operation_type=operation_type,
        )

        if wallet is None:
            existing_wallet = await self.repository.get_by_id(
                wallet_id,
            )

            if existing_wallet is None:
                raise WalletNotFoundError(f"Wallet {wallet_id} not found")

            raise InsufficientFundsError(
                f"Insufficient funds in wallet {wallet_id}"
            )

        await self.session.commit()

        return wallet
