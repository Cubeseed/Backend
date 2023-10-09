from django.db import models
# pylint: disable=imported-auth-user
from django.contrib.auth.models import User
from django.utils import timezone
from cubeseed.purchase_orders.models import PurchaseOrder


class OrderTracker(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=(
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("completed", "Completed")
    ), default="pending")

    description = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.purchase_order} - {self.status}"


class FarmPlanner(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    short_description = models.CharField(max_length=200) # description about the PO
    order_tracker = models.ForeignKey(OrderTracker, on_delete=models.CASCADE, null=True, blank=True)
    order_status = models.CharField(max_length=20, choices=(
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("completed", "Completed")
    ), default="pending")
    timestamp = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.farmer.username}'s Farm Planner"

    def save(self, *args, **kwargs):
        if self.order_tracker:
            self.order_status = self.order_tracker.status
        super().save(*args, **kwargs)
