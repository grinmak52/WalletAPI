from sqlalchemy.ext.asyncio import AsyncSession

from models import Wallet
from repositories.wallet import WalletRepository


class WalletService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = WalletRepository(session)
        self.session = session

    async def create_wallet(self) -> Wallet:
        wallet = await self.repository.create()

        await self.session.commit()

        return wallet

    async def get_wallet(self, wallet_id) -> Wallet | None:
        return await self.repository.get_by_id(wallet_id)