from django.contrib import admin
from .models import ProcessStorage, DispatchedStorage

# Register your models here.
admin.site.register(ProcessStorage)
admin.site.register(DispatchedStorage)