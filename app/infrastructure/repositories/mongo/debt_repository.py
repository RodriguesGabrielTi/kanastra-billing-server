import logging
from typing import List, Set, Optional, Mapping, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import BulkWriteError

from domain.entities.debt import Debt
from domain.entities.debtor import Debtor
from domain.value_objects.due_date import DueDate
from domain.value_objects.email import Email
from domain.value_objects.government_id import GovernmentId
from infrastructure.database.schemas.debt import DebtSchema
from infrastructure.repositories.debt_repository import DebtRepository as DebtRepositoryI

logging = logging.getLogger(__name__)


class DebtRepository(DebtRepositoryI):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["kanastra_billing"].get_collection("billing_debts")

    async def get_existing_ids(self, ids: List[str]) -> Set[str]:
        existing_docs = await self.collection.find({"debt_id": {"$in": ids}}, {"debt_id": 1}).to_list(None)
        return {doc["debt_id"] for doc in existing_docs}

    async def insert_batch(self, debts: List[dict]):
        if not debts:
            logging.info("No documents to insert.")
            return

        try:
            debt_ids = [debt['debt_id'] for debt in debts]
            existing_ids = await self.get_existing_ids(debt_ids)

            new_debts = [debt for debt in debts if debt['debt_id'] not in existing_ids]
            if not new_debts:
                logging.info("No new documents to insert.")
                return

            await self.collection.insert_many(debts, ordered=False)
        except BulkWriteError as e:
            logging.warning(f"Some documents were skipped due to duplicates. Details: {e.details}")
        except Exception as e:
            logging.error(f"Error inserting batch into MongoDB: {e}")
            raise e

    async def get_by_id(self, debt_id: str) -> Optional[Debt]:
        document = await self.collection.find_one({"debt_id": debt_id})
        if not document:
            return None
        return self._convert_to_entity(document)

    async def update(self, debt: Debt):
        update_data = self._convert_to_document(debt)

        result = await self.collection.update_one({"debt_id": debt.id}, {"$set": update_data})
        if result.modified_count:
            logging.info(f"Debt {debt.id} successfully updated.")
        else:
            logging.warning(f"No changes were made for debt {debt.id}.")

    def _convert_to_document(self, debt: Debt) -> dict:
        return {
            "debt_id": debt.id,
            "amount": debt.amount,
            "due_date": debt.due_date.value.isoformat(),
            "debtor": {
                "name": debt.debtor.name,
                "email": str(debt.debtor.email),
                "government_id": debt.debtor.government_id.value,
            },
            "notification_sent": debt.notification_sent,
            "billet_generated": debt.billet_generated,
        }

    def _convert_to_entity(self, document: Mapping[str, Any]) -> Debt:
        debt_schema = DebtSchema(**document)
        return Debt(
            id=debt_schema.id,
            government_id=GovernmentId(debt_schema.government_id),
            amount=debt_schema.amount,
            due_date=DueDate(debt_schema.due_date),
            debtor=Debtor(
                name=debt_schema.debtor.name,
                email=Email(debt_schema.debtor.email),
            ),
            notification_sent=debt_schema.notification_sent,
            billet_generated=debt_schema.billet_generated,
        )
