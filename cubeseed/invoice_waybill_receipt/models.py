from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# import userprofile model
from cubeseed.userprofile.models import UserProfile

User = get_user_model()

class Invoice(models.Model):
    payment_due_date = models.DateField()
    notes = models.TextField()
    signature = models.ImageField(upload_to='signatures/', blank=False, null=False)
    sent = models.BooleanField(default=False)
    invoice_date = models.DateTimeField(auto_now_add=True)
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, default="")
    delivered_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=False, null=False, default="")
    service = models.CharField(max_length=100, blank=False, null=False, default="")
    service_details = models.TextField(blank=False, null=False, default="")
    quantity = models.IntegerField(blank=False, null=False, default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, default=0.00)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, default=0.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, default=0.00)


class Waybill(models.Model):
    delivery_date = models.DateField()
    delivery_guy_first_name = models.CharField(max_length=100)
    delivery_guy_last_name = models.CharField(max_length=100)
    vehicle_name = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    vehicle_license_number = models.CharField(max_length=100)
    insurer_name = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=100)
    delivery_notes = models.TextField()
    signature = models.ImageField(upload_to='signatures/')
    sent = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

class Receipt(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=100)
    payment_notes = models.TextField()
    signature = models.ImageField(upload_to='signatures/')
    sent = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
