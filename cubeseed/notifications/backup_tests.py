from django.test import TestCase
from unittest import mock
from django.test import TestCase
from .tasks import send_email_notification, background_email_task


class TestSendEmailNotification(TestCase):
    def setUp(self):
        self.sender = {"email": "tester@cubeseed.com", "first_name": "Tester"}
        self.recipients = ["test_farmer_1@email_1.com", "test_farmer_1@email_2.com"]
        self.subject = "Account Approved!"
        self.email_category = "ACCOUNT_APPROVAL"

    def test_send_email_notification_success(self):
        from django.conf import settings

        FROM_EMAIL: str = settings.EMAIL_HOST_USER
        with mock.patch("django.core.mail.send_mail") as mock_send_mail:
            mock_send_mail.return_value = len(self.recipients)
            result = send_email_notification(
                self.sender, self.recipients, self.subject, self.email_category
            )
            self.assertTrue(result)
            mock_send_mail.assert_called_once_with(
                self.subject,
                "",
                FROM_EMAIL,
                self.recipients,
                fail_silently=False,
                html_message=mock.ANY,  # check that an HTML message is being sent
            )

    def test_send_email_notification_failure(self):
        with mock.patch("django.core.mail.send_mail") as mock_send_mail:
            mock_send_mail.return_value = 0
            result = send_email_notification(
                self.sender, self.recipients, self.subject, self.email_category
            )
            self.assertFalse(result)
            mock_send_mail.assert_called_once_with(
                self.subject,
                "",
                FROM_EMAIL,
                self.recipients,
                fail_silently=False,
                html_message=mock.ANY,  # check that an HTML message is being sent
            )


class TestBackgroundEmailTask(TestCase):
    def setUp(self):
        self.sender = {"email": "tester@cubeseed.com", "first_name": "Tester"}
        self.recipients = ["test_farmer_1@email_1.com", "test_farmer_1@email_2.com"]
        self.subject = "Account Approved!"
        self.email_category = "ACCOUNT_APPROVAL"

    def test_background_email_task_success(self):
        with mock.patch("django.core.mail.send_mail") as mock_send_mail:
            mock_send_mail.return_value = len(self.recipients)
            result = background_email_task(
                self.sender, self.recipients, self.subject, self.email_category
            )
            self.assertTrue(result.successful())
            mock_send_mail.assert_called_once_with(
                self.subject,
                "",
                self.sender["email"],
                self.recipients,
                fail_silently=False,
                html_message=mock.ANY,  # check that an HTML message is being sent
            )

    def test_background_email_task_failure(self):
        with mock.patch("django.core.mail.send_mail") as mock_send_mail:
            mock_send_mail.return_value = 0
            result = background_email_task(
                self.sender, self.recipients, self.subject, self.email_category
            )
            self.assertTrue(result.failed())
            mock_send_mail.assert_called_once_with(
                self.subject,
                "",
                self.sender["email"],
                self.recipients,
                fail_silently=False,
                html_message=mock.ANY,  # check that an HTML message is being sent
            )
