import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from application.use_cases.process_csv_billing import ProcessCsvBilling
from main import app

client = TestClient(app)


@pytest.fixture
def mock_process_csv_use_case():
    mock_use_case = AsyncMock(spec=ProcessCsvBilling)
    mock_use_case.execute.return_value = None
    return mock_use_case


def test_upload_csv_success(mock_process_csv_use_case, monkeypatch):
    monkeypatch.setattr("application.use_cases.process_csv_billing.ProcessCsvBilling.execute", mock_process_csv_use_case.execute)

    csv_content = b"debtId,governmentId,debtAmount,debtDueDate,name,email\n123,99999999999,1000,2025-12-31,John Doe,john@example.com"
    response = client.post("/billing/upload", files={"file": ("test.csv", csv_content)})

    assert response.status_code == 200
    assert response.json()["message"] == "File processed successfully"
    mock_process_csv_use_case.execute.assert_called_once()

