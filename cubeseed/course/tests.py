from rest_framework.test import APITestCase
from .models import Course
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


# Create your tests here.
class CourseAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Generate the token and add it to the auth header
        refresh = RefreshToken.for_user(self.user)
        self.token_value = str(refresh.access_token)

        self.auth_header = f"Bearer {self.token_value}"

        self.course = Course.objects.create(
            title='Test Course',
            description='Test Course Description',
            course_link='https://www.google.com/',
            is_required=True
        )

    def test_get_course_list(self):
        url = reverse("course-list")
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_course_detail(self):
        url = reverse("course-detail", args=[self.course.id])
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course(self):
        url = reverse("course-list")
        data = {
            "title": "New Course",
            "description": "New Course Description",
            "course_link": "https://www.example.com/",
            "is_required": True
        }
        response = self.client.post(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_course(self):
        url = reverse("course-detail", args=[self.course.id])
        data = {
            "title": "Updated Course",
            "description": "Updated Course Description",
            "course_link": "https://www.example.com/",
            "is_required": True
        }
        response = self.client.put(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
