from pydantic import BaseModel


class DebtorSchema(BaseModel):
    name: str
    email: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
