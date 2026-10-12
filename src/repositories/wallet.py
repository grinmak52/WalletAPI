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