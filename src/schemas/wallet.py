import uuid
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class WalletCreate(BaseModel):
    """Данные для создания кошелька."""

    model_config = ConfigDict(extra="forbid")


class WalletRead(BaseModel):
    """Данные кошелька в ответе API."""

    model_config = ConfigDict(from_attributes=True)

    wallet_id: uuid.UUID = Field(validation_alias="id")
    balance: Decimal