from pydantic import BaseModel, Field
from datetime import datetime

from infrastructure.database.schemas.debtor import DebtorSchema


class DebtSchema(BaseModel):
    id: str = Field(..., alias="_id")
    government_id: str
    amount: float
    due_date: datetime
    debtor: DebtorSchema
    notification_sent: bool = Field(default=False)
    billet_generated: bool = Field(default=False)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
