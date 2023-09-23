from os.path import splitext
from django.db import models
from django.core import exceptions
# pylint: disable=imported-auth-user
from django.contrib.auth.models import User

# To check if the file is only in PDF format
def validate_pdf_extension(value):
    ext = splitext(value.name)[1]  # Use the splitext function
    valid_extensions = [".pdf"]
    if ext.lower() not in valid_extensions:
        raise exceptions.ValidationError("Only PDF files are allowed.")

class CourseVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, blank=True, null=True)
    certificate = models.FileField(upload_to="certificates/", validators=[validate_pdf_extension])
    is_under_evaluation = models.BooleanField(default=True)
    approval_email_sent = models.BooleanField(default=False)
