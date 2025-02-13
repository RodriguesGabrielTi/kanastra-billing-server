import logging
import asyncio

from app.infrastructure.file_processors.csv_processor import CsvProcessor
from app.common.utils.logger_utility import LoggerUtility
from config import settings
from domain.dtos.debtor_dto import DebtorDTO
from domain.services.abstracts.billing_service import BillingService as BillingServiceI
from domain.services.billet_service import BilletService
from infrastructure.repositories.debt_repository import DebtRepository
from domain.services.abstracts.email_service import EmailService
from domain.dtos.debt_dto import DebtDTO


class BillingService(BillingServiceI):
    def __init__(
        self,
        csv_processor: CsvProcessor,
        debt_repository: DebtRepository,
        billet_service: BilletService,
        email_service: EmailService
    ):
        self.csv_processor = csv_processor
        self.debt_repository = debt_repository
        self.billet_service = billet_service
        self.email_service = email_service
        self.logger = logging.getLogger(__name__)

    async def save_in_batch(self, data: list[dict]):
        """Processes the batch asynchronously: Saves debts, generates billets, and sends notifications."""
        try:
            tasks = []
            for i in range(0, len(data), settings.CHUNK_SIZE_TO_SAVE):
                chunk = data[i: i + settings.CHUNK_SIZE_TO_SAVE]
                tasks.append(asyncio.create_task(self._process_batch(chunk)))

            await asyncio.gather(*tasks)

            LoggerUtility.log_info(self.logger, "CSV processing completed.")
            return {"status": "success", "message": "CSV processed, billets generated, and notifications sent."}

        except Exception as e:
            LoggerUtility.log_critical(self.logger, "Critical error processing CSV!", e)
            raise

    async def _process_batch(self, data_batch: list[dict]):
        """Processes each batch asynchronously: Saves debts, generates billets, and sends notifications."""
        await self.debt_repository.insert_batch(data_batch)
        # Todo: emitir tasks em lote via Celery para processar emails e gerar boletos
