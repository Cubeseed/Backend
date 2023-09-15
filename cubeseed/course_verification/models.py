from django.db import models
from django.contrib.auth.models import User
import os
from django.core.exceptions import ValidationError


# To check if the file is only pdf format
def validate_pdf_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".pdf"]
    if ext.lower() not in valid_extensions:
        raise ValidationError("Only PDF files are allowed.")

class courseVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, blank=True, null=True)
    certificate = models.FileField(upload_to="certificates/", validators=[validate_pdf_extension])
    is_under_evaluation = models.BooleanField(default=True)
    approval_email_sent = models.BooleanField(default=False)