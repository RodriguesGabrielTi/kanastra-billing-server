from dataclasses import dataclass

from domain.value_objects.email import Email
from domain.value_objects.government_id import GovernmentId


@dataclass(frozen=True)
class Debtor:
    name: str
    email: Email
    government_id: GovernmentId
