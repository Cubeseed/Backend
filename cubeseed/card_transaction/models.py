from django.db import models
# pylint: disable=imported-auth-user
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from cryptography.fernet import Fernet


class PaymentCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_holder_name = models.CharField(max_length=100)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=3)


    def __str__(self):
        return f"{self.user.username}'s Card"

    # validate card details
    def validate_card(self):
        # use Luhn's algorithm
        card_number = str(self.card_number).replace(" ", "") # Remove any spaces
        if not card_number.isdigit():
            raise ValidationError("Card number must be numeric digits only!!")

        reversed_digits = card_number[::-1]
        total = 0

        for i, digit in enumerate(reversed_digits):
            if i % 2 == 1:
                doubled = int(digit) * 2
                if doubled > 9:
                    doubled = doubled - 9
                total += doubled
            else:
                total += int(digit)

        if total % 10 != 0:
            raise ValidationError("Invalid card number. Please check and try again")

    def encrypt_card(self):
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)

        # encrypt card number and cvv
        encrypted_card_number = cipher_suite.encrypt(str(self.card_number).encode())
        encrypted_cvv = cipher_suite.encrypt(str(self.cvv).encode())

        # save encrypted card number and cvv
        self.card_number = encrypted_card_number.decode()
        self.cvv = encrypted_cvv.decode()
        self.save()

        return "Card details encrypted successfully"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s Transaction"


class CardTransaction(models.Model):
    card = models.ForeignKey(PaymentCard, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.card.card_number} - Transaction: {self.transaction}"

class PaymentGateway(models.Model):
    """A model to store payment gateway details"""
    name = models.CharField(max_length=100)
    url = models.URLField()
    api_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
