from django.db import models

from cubeseed.userprofile.models import UserProfile


class FarmerProfile(UserProfile):
    REVIEW_STATUSES = (
        ('P', 'PENDING'),
        ('R', 'REJECTED'),
        ('A', 'APPROVED')
    )

    review_status = models.CharField(max_length=1, choices=REVIEW_STATUSES)
