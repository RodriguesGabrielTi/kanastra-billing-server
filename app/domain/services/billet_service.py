import logging

from common.errors.internal_exceptions import BilletAlreadyGenerated
from domain.dtos.debt_dto import DebtDTO
from infrastructure.billets.billet_generator import BilletGenerator

logger = logging.getLogger(__name__)


class BilletService:
    def __init__(self, billet_generator: BilletGenerator):
        self.billet_generator = billet_generator

    def generate(self, debit: DebtDTO):
        if debit.billet_generated:
            raise BilletAlreadyGenerated(debit.debt_id)
        try:
            self.billet_generator.generate(debit)
        except Exception as e:
            logger.error(f"Error to generate Billet {debit.debt_id}: {e}")
            raise
