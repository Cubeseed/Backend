from django.contrib import admin
from .models import Invoice, Waybill, Receipt

# Register your models here.
admin.site.register(Invoice)
admin.site.register(Waybill)
admin.site.register(Receipt)
