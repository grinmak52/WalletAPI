from uuid import UUID
from decimal import Decimal

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Wallet


class WalletRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self) -> Wallet:
        wallet = Wallet()
        self.session.add(wallet)

        await self.session.flush()
        await self.session.refresh(wallet)

        return wallet

    async def get_by_id(self, wallet_id):
        return await self.session.get(Wallet, wallet_id)

    async def apply_operation(
            self,
            wallet_id: UUID,
            amount: Decimal,
            operation_type: str,
    ) -> Wallet | None:
        statement = update(Wallet).where(
            Wallet.id == wallet_id,
        )

        if operation_type == "DEPOSIT":
            statement = statement.values(
                balance=Wallet.balance + amount,
            )
        else:
            statement = statement.where(
                Wallet.balance >= amount,
            ).values(
                balance=Wallet.balance - amount,
            )

        statement = statement.returning(Wallet)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()
