from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery_app.conf.task_routes = {
    "application.tasks.create_debt_task.py": {"queue": "create_debt_task.py"},
    "application.tasks.send_email": {"queue": "email_queue"},
}
