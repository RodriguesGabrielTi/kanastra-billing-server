from dataclasses import dataclass
from uuid import UUID

from domain.value_objects.due_date import DueDate


@dataclass(frozen=True)
class Debt:
    id: UUID | str
    amount: float
    due_date: DueDate
    debtor: 'Debtor'
    notification_sent: bool = False
    billet_generated: bool = False
