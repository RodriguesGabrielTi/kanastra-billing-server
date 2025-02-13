import logging

from common.errors.internal_exceptions import EmailAlreadySentTo
from domain.dtos.debt_dto import DebtDTO
from domain.entities.debt import Debt
from domain.services.abstracts.email_service import EmailService as EmailServiceI
from infrastructure.email.sender import EmailSender

logger = logging.getLogger(__name__)


class EmailService(EmailServiceI):
    def __init__(self, email_sender: EmailSender):
        super().__init__(email_sender)

    def send(self, email: str, debit: DebtDTO):
        if debit.notification_sent:
            raise EmailAlreadySentTo(email)
        try:
            self.email_sender.send(email)
        except Exception as e:
            logger.error(f"Error sending email to {email}: {e}")
            raise
