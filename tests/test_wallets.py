from uuid import uuid4

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    ("operation_type", "amount", "expected_status"),
    [
        ("DEPOSIT", "100.00", 200),
        ("WITHDRAW", "0.00", 422),
        ("WITHDRAW", "-10.00", 422),
        ("TRANSFER", "10.00", 422),
        ("DEPOSIT", "1.234", 422),
    ],
)
async def test_wallet_operations(
    client: AsyncClient,
    operation_type: str,
    amount: str,
    expected_status: int,
) -> None:
    response = await client.post("/api/v1/wallets")
    assert response.status_code == 201

    wallet_id = response.json()["wallet_id"]

    response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={
            "operation_type": operation_type,
            "amount": amount,
        },
    )

    assert response.status_code == expected_status


async def test_create_wallet(client: AsyncClient) -> None:
    response = await client.post("/api/v1/wallets")

    assert response.status_code == 201

    data = response.json()
    assert data["balance"] == "0.00"
    assert data["wallet_id"]


async def test_get_wallet_balance(client: AsyncClient) -> None:
    created = await client.post("/api/v1/wallets")
    wallet_id = created.json()["wallet_id"]

    await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={
            "operation_type": "DEPOSIT",
            "amount": "150.00",
        },
    )

    response = await client.get(
        f"/api/v1/wallets/{wallet_id}",
    )

    assert response.status_code == 200
    assert response.json()["balance"] == "150.00"


async def test_wallet_not_found(client: AsyncClient) -> None:
    response = await client.get(
        f"/api/v1/wallets/{uuid4()}",
    )

    assert response.status_code == 404


async def test_insufficient_funds(client: AsyncClient) -> None:
    created = await client.post("/api/v1/wallets")
    wallet_id = created.json()["wallet_id"]

    response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={
            "operation_type": "WITHDRAW",
            "amount": "1.00",
        },
    )

    assert response.status_code == 409

    balance = await client.get(
        f"/api/v1/wallets/{wallet_id}",
    )

    assert balance.json()["balance"] == "0.00"
