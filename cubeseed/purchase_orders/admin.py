from django.contrib import admin
from .models import PurchaseOrder, OpenedPurchaseOrder

# Register your models here.
admin.site.register(PurchaseOrder)
admin.site.register(OpenedPurchaseOrder)
