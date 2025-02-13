
from application.tasks.send_email import send_email_task
from domain.entities.debt import Debt
from domain.entities.debtor import Debtor
from domain.value_objects.email import Email
from domain.value_objects.government_id import GovernmentId
from domain.value_objects.due_date import DueDate
import uuid
from datetime import datetime

from container import Container
from infrastructure.messages.celery import celery_app


@celery_app.task(bind=True, name='create_debt_task')
def create_debt_task(self, debt_data):
    # TODO: Mover para um serviço de dominio e finalizar implementação em batch
    try:
        container = Container()
        debt_repo = container.debt_repository()
        debtor_repo = container.debtor_repository()

        debtor_email = debt_data["debtor"]["email"]
        debtor = debtor_repo.get_or_create(debtor_email)

        if not debtor:
            debtor = Debtor(
                id=uuid.UUID(debt_data["debtor"]["id"]),
                name=debt_data["debtor"]["name"],
                email=Email(debtor_email),
            )
            debtor_repo.save(debtor)

        if not debt_repo.exists(debt_data["debt_id"]):
            debt = Debt(
                id=uuid.UUID(debt_data["debt_id"]),
                government_id=GovernmentId(debt_data["government_id"]),
                amount=float(debt_data["amount"]),
                due_date=DueDate(datetime.strptime(debt_data["debt_due_date"], "%Y-%m-%d").date()),
                debtor=debtor
            )
            debt_repo.save(debt)

            send_email_task.delay(debtor.email.value, debt.id)

        return {"status": "success", "debt_id": debt_data["debt_id"]}

    except Exception as e:
        return {"status": "error", "message": str(e)}
