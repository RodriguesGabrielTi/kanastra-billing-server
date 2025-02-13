from pydantic import BaseModel, EmailStr


class DebtorDTO(BaseModel):
    name: str
    email: EmailStr
    government_id: str
