from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime
from domain.dtos.debtor_dto import DebtorDTO


class DebtDTO(BaseModel):
    debt_id: str
    amount: float
    due_date: datetime
    debtor: Optional[DebtorDTO]
    notification_sent: bool = Field(default=False)
    billet_generated: bool = Field(default=False)
