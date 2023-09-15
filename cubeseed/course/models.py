from django.db import models
from cubeseed.course_verification.models import courseVerification


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    course_link = models.URLField()
    is_required = models.BooleanField(default=True)
    verifications = models.ManyToManyField(courseVerification, related_name="courses", blank=True)

    def __str__(self):
        return self.title