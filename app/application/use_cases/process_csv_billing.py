from typing import BinaryIO

from application.use_cases.use_case import UseCase
from infrastructure.file_processors.csv_processor import CsvProcessor


class ProcessCsvBilling(UseCase):
    def __init__(self, billing_service, csv_processor: CsvProcessor):
        self.billing_service = billing_service
        self.csv_processor = csv_processor

    async def execute(self, file: BinaryIO):
        data = self.csv_processor.process(
            file,
            {
                "debtId": "debt_id",
                "governmentId": "government_id",
                "debtAmount": "amount",
                "debtDueDate": "due_date",
                "name": "debtor_name",
                "email": "debtor_email"
            },
            {"governmentId": str, "debtDueDate": str},
        )

        await self.billing_service.save_in_batch(data)
