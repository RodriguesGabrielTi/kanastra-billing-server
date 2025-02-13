from abc import ABC, abstractmethod
from typing import List, Dict

from domain.entities.debt import Debt


class DebtRepository(ABC):
    """Generic Interface for Debt repositories"""

    @abstractmethod
    async def insert_batch(self, debts: List[Dict]):
        pass

    @abstractmethod
    async def get_existing_ids(self, debt_ids: List[str]) -> set:
        pass

    @abstractmethod
    async def update(self, debt: Debt) -> set:
        pass
