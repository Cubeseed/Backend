from django.contrib import admin
from .models import Room, Message
# from .models import Conversation

# Register your models here.
admin.site.register(Room)
# admin.site.register(Converation)
admin.site.register(Message)