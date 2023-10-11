"""
This module contains tasks for sending notifications asynchronously using Celery.
"""

import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from logging import StreamHandler, Logger
from celery import shared_task, signals
from celery.signals import setup_logging
from celery.result import AsyncResult
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from cubeseed.celery import app as celery_app

# Email settings
FROM_EMAIL: str = settings.EMAIL_HOST_USER
RECIPIENT_LIST: list = [
    "cubeseed-tester@mailinator.com",
]

# Retry policy for failed tasks
RETRY_POLICY: dict = {
    "max_retries": 3,
    "interval_start": 0,
    "interval_step": 0.2,
    "interval_max": 0.5,
}

# Test user for sending emails
TEST_USER: dict = ({"email": FROM_EMAIL, "first_name": "cubeseed-tester"},)

# HTML Email templates
EMAIL_TEMPLATES: dict = {
    "ACCOUNT_APPROVAL": "mail/account_approval.html",
    "ACCOUNT_REJECTION": "mail/account_rejection.html",
    "ACCOUNT_CREATION": "mail/account_creation.html",
    "ACCOUNT_DELETION": "mail/account_deletion.html",
    "ACCOUNT_UPDATE": "mail/account_update.html",
    "ACCOUNT_PASSWORD_RESET": "mail/password_reset.html",
    "ACCOUNT_PASSWORD_CHANGE": "mail/password_change.html",
    "DOCUMENT_APPROVAL": "mail/document_approval.html",
    "DOCUMENT_REJECTION": "mail/document_rejection.html",
}

# Logger for Celery tasks
logger: Logger = logging.getLogger("celery")


@setup_logging.connect
def configure_celery_logging(sender, **kwargs) -> None:
    """
    Configures the Celery logger with a rotating file handler and a console handler.
    The file handler rotates the log file when it reaches a maximum size of 10000 bytes
    and keeps a maximum of 5 backup files. The console handler logs only errors.

    Args:
        sender: The sender of the signal.
        kwargs: Additional keyword arguments.
    """
    # Configure the Celery logger
    task_logger = logging.getLogger("celery")
    # Create a rotating file handler
    file_handler = RotatingFileHandler("celery.log", maxBytes=10000, backupCount=5)
    # Create a console handler
    console_handler = StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    # Set the log format for both handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.ERROR)
    # Add both handlers to the logger
    task_logger.addHandler(file_handler)
    task_logger.addHandler(console_handler)


@signals.task_prerun.connect
def task_prerun(*args, **kwargs) -> None:
    """
    Logs a message when a task is about to start.

    Args:
        args: Additional positional arguments.
        kwargs: Additional keyword arguments.
    """
    logger.info(f'Task ({kwargs["task_id"]}): {kwargs["task"].name} is about to start.')


@signals.task_success.connect
def task_success(*args, **kwargs) -> None:
    """
    Logs a message when a task succeeds.

    Args:
        args: Additional positional arguments.
        kwargs: Additional keyword arguments.
    """
    logger.info(f"Task succeeded!")


@signals.task_failure.connect
def task_failure(*args, **kwargs) -> None:
    """
    Logs a message when a task fails.

    Args:
        args: Additional positional arguments.
        kwargs: Additional keyword arguments.
    """
    logger.error(f"Task failed!")


@shared_task
def send_email_notification(
    sender: dict, recipients: list, subject: str, email_category: str
) -> bool:
    """
    Sends an email notification to the specified recipients.

    Args:
        sender (dict): The sender object.
        recipients (list): A list of email addresses of the recipients.
        subject (str): The subject of the email.
        email_category (str): The category of the email.

    Returns:
        bool: True if the mail was successfully delivered to all recipients, False otherwise.
    """
    HTML_MESSAGE = render_to_string(
        EMAIL_TEMPLATES[email_category],
        {
            "user": sender,
            "current_datetime": datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S"),
            "support_email": FROM_EMAIL,
        },
    )
    receipt_count: int = send_mail(
        subject,
        "",
        FROM_EMAIL,
        recipients,
        fail_silently=False,
        html_message=HTML_MESSAGE,
    )
    return receipt_count == len(recipients)


def background_email_task(
    sender: dict = TEST_USER,
    recipients: list = RECIPIENT_LIST,
    subject: str = "Test Email",
    email_category: str = "ACCOUNT_APPROVAL",
) -> AsyncResult:
    """
    Sends an email notification asynchronously using Celery.

    Args:
        sender (str): The email address of the sender. Defaults to TEST_USER.
        recipients (list): A list of email addresses of the recipients. Defaults to RECIPIENT_LIST.
        subject (str): The subject of the email. Defaults to "Test Email".
        email_category (str): The category of the email. Defaults to "ACCOUNT_APPROVAL".

    Returns:
        AsyncResult: The result of the asynchronous task.
    """
    task = send_email_notification.apply_async(
        args=(sender, recipients, subject, email_category),
        retry=True,
        retry_policy=RETRY_POLICY,
    )
    result: AsyncResult = celery_app.AsyncResult(task.id)
    return result
