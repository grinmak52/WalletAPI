import uuid
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class OperationType(StrEnum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class WalletOperation(BaseModel):
    """Операции с кошельком"""

    model_config = ConfigDict(extra="forbid")

    operation_type: OperationType
    amount: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2,
    )


class WalletCreate(BaseModel):
    """Данные для создания кошелька."""

    model_config = ConfigDict(extra="forbid")


class WalletRead(BaseModel):
    """Данные кошелька в ответе API."""

    model_config = ConfigDict(from_attributes=True)

    wallet_id: uuid.UUID = Field(validation_alias="id")
    balance: Decimal
