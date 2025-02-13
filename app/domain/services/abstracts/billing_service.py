from abc import ABC, abstractmethod
from typing import List, Dict


class BillingService(ABC):
    @abstractmethod
    async def save_in_batch(self, data: List[Dict]) -> Dict[str, str]:
        """Processes and stores data in batches"""
        raise NotImplementedError("Subclass must implement this method")
