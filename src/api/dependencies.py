from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from services.wallet import WalletService


SessionDep = Annotated[AsyncSession, Depends(db_helper.session_getter)]


def get_wallet_service(
    session: SessionDep,
) -> WalletService:
    return WalletService(session)


WalletServiceDep = Annotated[
    WalletService,
    Depends(get_wallet_service),
]