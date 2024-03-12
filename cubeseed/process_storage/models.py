import uuid

from django.contrib.auth.models import User
from cubeseed.address.models import Address
from django.db import models

# Create your Process Storage models here.
class ProcessStorage(models.Model):
    """ Create your Process Storage models here. """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.CharField(max_length=255)
    services = models.CharField(max_length=255)
    paymentdetails = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location

# Create your Dispatched Storage models here.
class DispatchedStorage(models.Model):
    """ Create your Dispatched Storage models here. """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    driver_name = models.CharField(max_length=255)
    vehical_id = models.CharField(max_length=255)
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    farmer_location = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)
    invoice_id = models.CharField(max_length=255)
    receipt_id = models.CharField(max_length=255)
    waybill_id = models.CharField(max_length=255)
    grn_id = models.CharField(max_length=255)
    goods_received_note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.farmer.username} - {self.driver_name}"