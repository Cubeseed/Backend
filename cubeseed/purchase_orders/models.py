import uuid
# pylint: disable=imported-auth-user
from django.contrib.auth.models import User

from django.db import models


# For creating the purchase order
class PurchaseOrder(models.Model):
    name = models.CharField(max_length=255)
    order_number = models.CharField(max_length=32, unique=True, default=uuid.uuid4, editable=False)
    date_sent = models.DateField()
    delivery_date = models.DateField()
    delivery_venue = models.CharField(max_length=255)
    products = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    buyer_name = models.CharField(max_length=255)
    terms_and_conditions = models.TextField()
    status = models.CharField(max_length=20, choices=(
                                                      ("pending", "Pending"),
                                                      ("accepted", "Accepted"),
                                                      ("rejected", "Rejected")), default="pending")
    accepted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="accepted_orders")

    def __str__(self):
        return f"{self.name}"


class OpenedPurchaseOrder(models.Model):
    """Orders opened by the farmer"""
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.farmer.username} - {self.purchase_order.name}"
