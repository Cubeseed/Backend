from django.db import models
from django.conf import settings


# Your existing document type choices
BUSINESS_DOCUMENT_TYPES = (
    ('TIN', 'Tax Identification Number'),
    ('PITIN', 'Personal Income Tax Identification Number'),
    ('CAC_CERTIFICATE', 'CAC Certificate'),
    ('OTHER', 'Other Document')
)

class BusinessProfile(models.Model):
    url = models.URLField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    telephone = models.CharField(max_length=50)
    billing_address = models.CharField(max_length=128)
    shipping_address = models.CharField(max_length=128)
    logo = models.ImageField(upload_to='business_logos/', null=True, blank=True)
    document_type = models.CharField(max_length=20, choices=BUSINESS_DOCUMENT_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

