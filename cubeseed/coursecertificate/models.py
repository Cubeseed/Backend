from django.db import models

from cubeseed.userprofile.models import UserProfile


class CourseCertificate(models.Model):
    REVIEW_STATUSES = (
        ('P', 'PENDING'),
        ('R', 'REJECTED'),
        ('A', 'APPROVED')
    )

    name = models.CharField(max_length=100)
    review_status = models.CharField(max_length=1, choices=REVIEW_STATUSES)
    reviewed_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # shouldn't be models.CASCADE
    reviewed_date = models.DateField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # user this certificate belongs to

    def __str__(self):
        return self.user.full_name + " - " + self.name + " - " + self.get_review_status_display()
