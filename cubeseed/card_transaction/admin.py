from django.contrib import admin
from .models import PaymentCard, CardTransaction, PaymentGateway, Transaction

# Register your models here.
admin.site.register(PaymentCard)
admin.site.register(CardTransaction)
admin.site.register(PaymentGateway)
admin.site.register(Transaction)
