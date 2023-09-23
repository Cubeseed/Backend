from rest_framework.test import APITestCase
from .models import CourseVerification
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status


# Create your tests here.
class courseVerificationTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # generate the token and add it to the auth header
        refresh = RefreshToken.for_user(self.user)
        self.token_value = str(refresh.access_token)
        self.auth_header = f"Bearer {self.token_value}"

    def test_create_course_verification(self):
        certificate_file = SimpleUploadedFile(
            name="test_certificate.pdf",
            content=b"pdf_file_content",
            content_type="application/pdf"
        )

        url = reverse("courseverification-list")
        data = {
            "user": self.user.id,
            "certificate": certificate_file
        }
        response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CourseVerification.objects.count(), 1)

    def test_invalid_certificate_extension(self):
        # create a certificate with invalid extension
        invalid_certificate_file = SimpleUploadedFile(
            name="test_certificate.txt",
            content=b"txt_file_content",
            content_type="text/plain"
        )

        url = reverse("courseverification-list")
        data = {
            "user": self.user.id,
            "certificate": invalid_certificate_file
        }

        respose = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(respose.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CourseVerification.objects.count(), 0)

    def test_valid_certificate_extension(self):
        # create a certificate with valid extension
        valid_certificate_file = SimpleUploadedFile(
            name="test_certificate.pdf",
            content=b"pdf_file_content",
            content_type="application/pdf"
        )

        url = reverse("courseverification-list")
        data = {
            "user": self.user.id,
            "certificate": valid_certificate_file
        }

        respose = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(respose.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CourseVerification.objects.count(), 1)
