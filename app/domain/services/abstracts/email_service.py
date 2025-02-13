import logging
from abc import ABC, abstractmethod

from domain.dtos.debt_dto import DebtDTO
from domain.entities.debt import Debt
from infrastructure.email.sender import EmailSender

logger = logging.getLogger(__name__)


class EmailService(ABC):
    def __init__(self, email_sender: EmailSender):
        self.email_sender = email_sender

    @abstractmethod
    def send(self, email: str, debit: DebtDTO):
        raise NotImplementedError("Subclass must implement this method")
