from django.contrib import admin
from .models import FarmPlanner, OrderTracker

# Register your models here.
admin.site.register(FarmPlanner)
admin.site.register(OrderTracker)
