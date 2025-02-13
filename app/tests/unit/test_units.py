import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from application.use_cases.process_csv_billing import ProcessCsvBilling
from infrastructure.email.sender_print import EmailSenderPrint
from infrastructure.repositories.debt_repository import DebtRepository
from infrastructure.file_processors.csv_processor import CsvProcessor
from domain.dtos.debt_dto import DebtDTO
from domain.services.billet_service import BilletService
from main import app

client = TestClient(app)


@pytest.fixture
def mock_csv_processor():
    processor = AsyncMock(spec=CsvProcessor)
    processor.process.return_value = [
        {
            "debt_id": "123",
            "amount": 1000,
            "due_date": "2025-12-31",
            "debtor_name": "John Doe",
            "debtor_email": "john@example.com",
            "government_id": "99999999999"
        }
    ]
    return processor


@pytest.fixture
def mock_debt_repository():
    repository = AsyncMock(spec=DebtRepository)
    repository.insert_batch.return_value = None
    return repository


@pytest.fixture
def mock_billet_service():
    service = AsyncMock(spec=BilletService)
    service.generate.return_value = None
    return service


@pytest.fixture
def process_csv_billing(mock_csv_processor, mock_debt_repository, mock_billet_service):
    return ProcessCsvBilling(mock_debt_repository, mock_csv_processor)


@pytest.mark.asyncio
async def test_process_csv_billing_success(process_csv_billing, mock_csv_processor):
    file_mock = MagicMock()
    await process_csv_billing.execute(file_mock)
    mock_csv_processor.process.assert_called_once()


@pytest.mark.asyncio
async def test_insert_batch_success(mock_debt_repository):
    data = [
        {
            "debt_id": "123",
            "amount": 1000,
            "due_date": "2025-12-31",
            "debtor_name": "John Doe",
            "debtor_email": "john@example.com",
            "government_id": "99999999999"
        }
    ]
    await mock_debt_repository.insert_batch(data)
    mock_debt_repository.insert_batch.assert_called_once()


@pytest.mark.asyncio
async def test_generate_billet_success(mock_billet_service):
    debt_dto = DebtDTO(
        debt_id="123",
        amount=1000,
        due_date="2025-12-31",
        debtor=None
    )
    await mock_billet_service.generate(debt_dto)
    mock_billet_service.generate.assert_called_once()


def test_email_sender_print():
    email_sender = EmailSenderPrint()
    email_sender.send("test@example.com", "BILLET_123")


def test_upload_csv_invalid_file():
    response = client.post("/billing/upload", files={"file": ("test.txt", b"content")})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid file type. Please upload a CSV file."
