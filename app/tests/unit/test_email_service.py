import pytest
from unittest.mock import MagicMock
from domain.dtos.debt_dto import DebtDTO
from infrastructure.email.sender import EmailSender
from domain.services.email_service import EmailService
from common.errors.internal_exceptions import EmailAlreadySentTo


@pytest.fixture
def mock_email_sender():
    return MagicMock(spec=EmailSender)


@pytest.fixture
def email_service(mock_email_sender):
    return EmailService(mock_email_sender)


def test_send_email_success(email_service, mock_email_sender):
    debt_dto = DebtDTO(
        debt_id="123",
        amount=1000,
        due_date="2025-12-31",
        debtor=None,
        notification_sent=False
    )

    email_service.send("test@example.com", debt_dto)
    mock_email_sender.send.assert_called_once_with("test@example.com")


def test_send_email_already_sent(email_service):
    debt_dto = DebtDTO(
        debt_id="123",
        amount=1000,
        due_date="2025-12-31",
        debtor=None,
        notification_sent=True
    )

    with pytest.raises(EmailAlreadySentTo):
        email_service.send("test@example.com", debt_dto)
