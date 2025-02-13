from dependency_injector import containers, providers
from motor.motor_asyncio import AsyncIOMotorClient

from application.use_cases.process_csv_billing import ProcessCsvBilling
from config import settings
from domain.services.billet_service import BilletService
from domain.services.billing_service import BillingService
from domain.services.email_service import EmailService
from infrastructure.billets.billet_generator import BilletGenerator
from infrastructure.email.sender_print import EmailSenderPrint
from infrastructure.file_processors.csv_processor import CsvProcessor
from infrastructure.repositories.mongo.debt_repository import DebtRepository


class Container(containers.DeclarativeContainer):
    mongo_client = providers.Singleton(AsyncIOMotorClient, settings.MONGO_URI)

    debt_repository = providers.Factory(DebtRepository, db=mongo_client)

    csv_processor = providers.Factory(CsvProcessor)
    billet_generator = providers.Factory(BilletGenerator)
    email_sender = providers.Factory(EmailSenderPrint)

    email_service = providers.Factory(EmailService, email_sender=email_sender)
    billet_service = providers.Factory(BilletService, billet_generator=billet_generator)

    billing_service = providers.Factory(
        BillingService, debt_repository=debt_repository, csv_processor=csv_processor, billet_service=billet_service, email_service=email_service
    )

    # Caso de Uso
    process_csv_use_case = providers.Factory(ProcessCsvBilling, billing_service=billing_service, csv_processor=csv_processor)
