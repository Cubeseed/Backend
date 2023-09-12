from celery import shared_task, signals
from .celery import app as celery_app
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
import logging
from datetime import datetime
from celery.result import AsyncResult

logger = logging.getLogger(__name__)


@signals.task_prerun.connect
def task_prerun(*args, **kwargs):
    logger.info(
        f'Task ({kwargs["task_id"]}): {kwargs["task"].name} is about to start.'
    )


@signals.task_success.connect
def task_success(*args, **kwargs):
    logger.info(f"Task succeeded!")


@signals.task_failure.connect
def task_failure(*args, **kwargs):
    logger.error(f"Task failed!")


FROM_EMAIL: str = settings.EMAIL_HOST_USER
RECIPIENT_LIST: list = [
    "cubeseed-tester@mailinator.com",
]
CURRENT_DATETIME: str = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
RETRY_POLICY: dict = {
    "max_retries": 3,
    "interval_start": 0,
    "interval_step": 0.2,
    "interval_max": 0.5,
}
TEST_USER: dict = ({"email": FROM_EMAIL, "first_name": "cubeseed-tester"},)


@shared_task
def send_approval_email(user):
    HTML_MESSAGE = render_to_string(
        "mail/approval_mail.html",
        {
            "user": user,
            "current_datetime": CURRENT_DATETIME,
            "support_email": FROM_EMAIL,
        },
    )
    print(HTML_MESSAGE)
    send_mail(
        "Your documents have been approved",
        "",
        FROM_EMAIL,
        RECIPIENT_LIST,
        fail_silently=False,
        html_message=HTML_MESSAGE,
    )


@shared_task
def send_rejection_email(user):
    HTML_MESSAGE = render_to_string(
        "mail/rejection_mail.html",
        {
            "user": user,
            "current_datetime": CURRENT_DATETIME,
            "support_email": FROM_EMAIL,
        },
    )
    send_mail(
        "Your documents have been rejected",
        "",
        FROM_EMAIL,
        RECIPIENT_LIST,
        fail_silently=False,
        html_message=HTML_MESSAGE,
    )


def approve_task(user=TEST_USER):
    task = send_approval_email.apply_async(
        args=(user,),
        retry=True,
        retry_policy=RETRY_POLICY,
    )
    result: AsyncResult = celery_app.AsyncResult(task.id)
    return result


def reject_task(user=TEST_USER):
    task = send_rejection_email.apply_async(
        args=(user,),
        retry=True,
        retry_policy=RETRY_POLICY,
    )
    result: AsyncResult = celery_app.AsyncResult(task.id)
    return result
