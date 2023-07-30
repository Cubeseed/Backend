from django.db import models
from django.core.files.storage import default_storage

from cubeseed.userprofile.models import UserProfile, FarmerProfile


class FileDescriptor(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # won't create a table for this class
        abstract = True

def upload_certificate(instance, filename):
    certificate_name = f"course_certificate/{instance.farmer_profile.user_profile.id}/{instance.name}"
    default_storage.delete(certificate_name)
    return certificate_name

class CourseCertificateFile(FileDescriptor):
    REVIEW_STATUSES = (
        ('P', 'PENDING'),
        ('R', 'REJECTED'),
        ('A', 'APPROVED')
    )

    review_status = models.CharField(max_length=1, choices=REVIEW_STATUSES, default='P')
    reviewed_by = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)
    reviewed_date = models.DateField(null=True, blank=True)
    farmer_profile = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE)
    certificate = models.FileField(upload_to=upload_certificate)

    def __str__(self):
        return self.farmer_profile.user_profile.full_name + " - " + self.name + " - " + self.get_review_status_display()