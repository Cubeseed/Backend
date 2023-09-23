from unittest.mock import patch, MagicMock
from datetime import datetime
from django.test import TestCase
from django.core.mail import send_mail
from .tasks import send_email_notification, background_email_task


class TestSendEmailNotification(TestCase):
    def setUp(self):
        self.sender = {"email": "tester@cubeseed.com", "first_name": "Tester"}
        self.recipients = ["test_farmer_1@email_1.com", "test_farmer_1@email_2.com"]
        self.subject = "Account Approved!"
        self.email_category = "ACCOUNT_APPROVAL"

    @patch("django.core.mail.send_mail")
    @patch("django.template.loader.render_to_string")
    def test_send_email_notification(self, mock_render_to_string, mock_send_mail):
        from django.conf import settings

        FROM_EMAIL: str = settings.EMAIL_HOST_USER
        mock_html_message = mock_render_to_string(
            "mail/account_approval.html",
            {
                "user": self.sender,
                "current_datetime": datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S"),
                "support_email": FROM_EMAIL,
            },
        )
        mock_send_mail.return_value = len(self.recipients)

        send_status: bool = send_email_notification(
            self.sender, self.recipients, self.subject, self.email_category
        )
        mock_send_mail.assert_called_once_with(
            self.subject,
            "",
            FROM_EMAIL,
            self.recipients,
            fail_silently=False,
            html_message=mock_html_message,
        )
        self.assertTrue(send_status)
        self.assertEqual(mock_render_to_string.call_count, 1)


class TestBackgroundEmailTask(TestCase):
    def setUp(self):
        self.sender = {"email": "tester@cubeseed.com", "first_name": "Tester"}
        self.recipients = ["test_farmer_1@email_1.com", "test_farmer_1@email_2.com"]
        self.subject = "Account Approved!"
        self.email_category = "ACCOUNT_APPROVAL"

    @patch("cubeseed.notifications.tasks.send_email_notification.apply_async")
    @patch("cubeseed.notifications.tasks.celery_app.AsyncResult")
    def test_background_email_task(self, mock_async_result, mock_apply_async):
        mock_task = MagicMock()
        mock_task.id = "test_task_id"
        mock_apply_async.return_value = mock_task
        mock_async_result.return_value = mock_task
        result = background_email_task(
            self.sender, self.recipients, self.subject, self.email_category
        )
        mock_apply_async.assert_called_once_with(
            args=(self.sender, self.recipients, self.subject, self.email_category),
            retry=True,
            retry_policy={
                "max_retries": 3,
                "interval_start": 0,
                "interval_step": 0.2,
                "interval_max": 0.5,
            },
        )
        mock_async_result.assert_called_once_with("test_task_id")
        self.assertEqual(result, mock_task)
