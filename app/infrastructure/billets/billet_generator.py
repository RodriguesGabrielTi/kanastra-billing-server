from domain.dtos.debt_dto import DebtDTO


class BilletGenerator:
    def generate(self, debit: DebtDTO):
        print(f"Generating Billet {debit.debt_id} with debit {debit.amount}")
