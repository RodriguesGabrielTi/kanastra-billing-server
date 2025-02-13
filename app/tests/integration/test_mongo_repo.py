import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from infrastructure.repositories.debt_repository import DebtRepository

@pytest.fixture
def test_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017/test_db")
    return client["test_db"]

@pytest.mark.asyncio
async def test_insert_and_retrieve_debt(test_db):
    repo = DebtRepository(test_db)

    debt_data = {
        "debt_id": "test123",
        "amount": 1000,
        "due_date": "2025-12-31",
        "debtor": {
            "name": "John Doe",
            "email": "john@example.com",
            "government_id": "99999999999"
        },
        "notification_sent": False,
        "billet_generated": False
    }

    await repo.insert_batch([debt_data])
    retrieved_debt = await repo.get_by_id("test123")

    assert retrieved_debt is not None
    assert retrieved_debt.amount == 1000
    assert retrieved_debt.debtor.email == "john@example.com"
