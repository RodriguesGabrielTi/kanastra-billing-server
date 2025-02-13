from infrastructure.messages.celery import celery_app


@celery_app.task(bind=True)
def send_email_task(self, email, debt_id):
    # todo: finish this to improve speed
    pass
