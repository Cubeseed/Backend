from django.db import models
from django.core.files.storage import default_storage

from cubeseed.userprofile.models import UserProfile
from cubeseed.filedescriptor.models import FileDescriptor


def save_to(instance, filename):
    certificate_name = f"course_certificate/{instance.user_profile.user.id}/{instance.name}"
    default_storage.delete(certificate_name)
    return certificate_name


class CourseCertificateFile(FileDescriptor):
    REVIEW_STATUSES = (
        ('P', 'PENDING'),
        ('R', 'REJECTED'),
        ('A', 'APPROVED')
    )

    review_status = models.CharField(max_length=1, choices=REVIEW_STATUSES)
    reviewed_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # shouldn't be models.CASCADE
    reviewed_date = models.DateField()
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # user this certificate belongs to
    certificate = models.FileField(upload_to=save_to)

    def __str__(self):
        return self.user_profile.full_name + " - " + self.name + " - " + self.get_review_status_display()
