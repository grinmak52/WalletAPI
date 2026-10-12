import asyncio

from httpx import AsyncClient


async def test_concurrent_deposits(
    client: AsyncClient,
) -> None:
    created = await client.post("/api/v1/wallets")
    wallet_id = created.json()["wallet_id"]

    async def deposit() -> int:
        response = await client.post(
            f"/api/v1/wallets/{wallet_id}/operation",
            json={
                "operation_type": "DEPOSIT",
                "amount": "10.00",
            },
        )
        return response.status_code

    results = await asyncio.gather(*(deposit() for _ in range(20)))

    assert results == [200] * 20

    response = await client.get(
        f"/api/v1/wallets/{wallet_id}",
    )

    assert response.status_code == 200
    assert response.json()["balance"] == "200.00"


async def test_concurrent_withdrawals(
    client: AsyncClient,
) -> None:
    created = await client.post("/api/v1/wallets")
    wallet_id = created.json()["wallet_id"]

    await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={
            "operation_type": "DEPOSIT",
            "amount": "100.00",
        },
    )

    async def withdraw() -> int:
        response = await client.post(
            f"/api/v1/wallets/{wallet_id}/operation",
            json={
                "operation_type": "WITHDRAW",
                "amount": "20.00",
            },
        )
        return response.status_code

    results = await asyncio.gather(*(withdraw() for _ in range(10)))

    assert results.count(200) == 5
    assert results.count(409) == 5

    response = await client.get(
        f"/api/v1/wallets/{wallet_id}",
    )

    assert response.status_code == 200
    assert response.json()["balance"] == "0.00"
