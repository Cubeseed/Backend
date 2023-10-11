from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import PaymentCard, PaymentGateway, Transaction, CardTransaction
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError


class PaymentCardAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Generate the token and add it to the auth header
        refresh = RefreshToken.for_user(self.user)
        self.token_value = str(refresh.access_token)
        self.auth_header = f"Bearer {self.token_value}"

        # Create a PaymentCard associated with the user
        self.payment_card = PaymentCard.objects.create(
            user = self.user,
            card_number = "4111111111111111",
            card_holder_name = "testuser",
            cvv = "123",
            expiry_date = "2023-08-27",
        )

    # Test GET all payment cards route
    def test_list_payment_cards(self):
        url = reverse("paymentcard-list")
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test POST(create) payment card route
    def test_create_payment_cards(self):
        url = reverse("paymentcard-list")
        data = {
            "user": self.user.id,
            "card_number": "1234567890123456",
            "card_holder_name": "testuser",
            "cvv": "123",
            "expiry_date": "2023-08-27"
        }
        response = self.client.post(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test GET payment card by id route
    def test_get_payment_cards_by_id(self):
        url = reverse("paymentcard-detail", args=[self.payment_card.id])
        response = self.client.get(url, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test PUT(update) payment card by id route
    def test_put_payment_card_by_id(self):
        url = reverse("paymentcard-detail", args=[self.payment_card.id])
        data = {
            "user": self.user.id,
            "card_number": "1234567890123456",
            "card_holder_name": "testuser",
            "cvv": "123",
            "expiry_date": "2023-08-27"
        }
        response = self.client.put(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the object from the database and check the updated data
        self.payment_card.refresh_from_db()
        self.assertEqual(self.payment_card.card_number, data["card_number"])
        self.assertEqual(self.payment_card.card_holder_name, data["card_holder_name"])
        self.assertEqual(self.payment_card.cvv, data["cvv"])
        self.assertEqual(self.payment_card.expiry_date.strftime("%Y-%m-%d"), data["expiry_date"])


    # Test DELETE payment card by id route
    def test_delete_payment_card_by_id(self):
        url = reverse("paymentcard-detail", args=[self.payment_card.id])
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test validate payment card
    def test_validate_payment_card(self):
        # create valid card
        try:
            PaymentCard.validate_card(self.payment_card)
        except ValidationError:
            self.fail("Validation should not have raised an exception for a valid card number")

    # Test encrypt card details
    def test_encrypt_card_details(self):
        try:
            PaymentCard.encrypt_card(self.payment_card)
        except Exception:
            self.fail("Encryption should not have raised an exception")

class PaymentGateWayAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Generate the token and add it to the auth header
        refresh = RefreshToken.for_user(self.user)
        self.token_value = str(refresh.access_token)
        self.auth_header = f"Bearer {self.token_value}"

        # Create a PaymentGateway associated with the user
        self.payment_gateway = PaymentGateway.objects.create(
            name = "testpaymentgateway",
            url = "https://example.com/pay",
            api_key = "1234key",
            secret_key = "12345"
        )

    # Test GET all payment gateways route
    def test_list_payment_gateways(self):
        url = reverse("paymentgateway-list")
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test GET payment gateway by id route
    def test_get_payment_gateways_by_id(self):
        url = reverse("paymentgateway-detail", args=[self.payment_gateway.id])
        response = self.client.get(url, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test POST(create) payment gateway route
    def test_create_payment_gateways(self):
        url = reverse("paymentgateway-list")
        data = {
            "name": "paymentgateway",
            "url": "https://example.com/new-pay",
            "api_key": "1234",
            "secret_key": "1234"
        }
        response = self.client.post(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PaymentGateway.objects.count(), 2)

    # Test PUT(update) payment gateway by id route
    def test_update_payment_gateway_by_id(self):
        url = reverse("paymentgateway-detail", args=[self.payment_gateway.id])
        data = {
            "name": "paymentgateway2",
            "url": "https://example.com/new-pay",
            "api_key": "1234",
            "secret_key": "1234"
        }
        response = self.client.put(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the object from the database and check the updated data
        self.payment_gateway.refresh_from_db()
        self.assertEqual(self.payment_gateway.name, data["name"])
        self.assertEqual(self.payment_gateway.url, data["url"])
        self.assertEqual(self.payment_gateway.api_key, data["api_key"])
        self.assertEqual(self.payment_gateway.secret_key, data["secret_key"])

    # Test PATCH(update) payment gateway by id route
    def test_patch_payment_gateway_by_id(self):
        url = reverse("paymentgateway-detail", args=[self.payment_gateway.id])
        data = {
            "name": "paymentgateway2",
            "url": "https://example.com/new-pay",
            "api_key": "1234",
            "secret_key": "123455"
        }
        response = self.client.patch(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the object from the database and check the updated data
        self.payment_gateway.refresh_from_db()
        self.assertEqual(self.payment_gateway.name, data["name"])
        self.assertEqual(self.payment_gateway.url, data["url"])
        self.assertEqual(self.payment_gateway.api_key, data["api_key"])
        self.assertEqual(self.payment_gateway.secret_key, data["secret_key"])

    # Test DELETE payment gateway by id route
    def test_delete_payment_gateway_by_id(self):
        url = reverse("paymentgateway-detail", args=[self.payment_gateway.id])
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class TransactionAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Generate the token and add it to the auth header
        refresh = RefreshToken.for_user(self.user)
        self.token_value = str(refresh.access_token)
        self.auth_header = f"Bearer {self.token_value}"

        # Create a Transaction associated with the user
        self.transaction = Transaction.objects.create(
            user = self.user,
            amount = 100,
            description = "test transaction",
            date = "2023-08-27"
        )

    # Test GET all transactions route
    def test_list_transactions(self):
        url = reverse("transaction-list")
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test GET transaction by id route
    def test_get_transactions_by_id(self):
        url = reverse("transaction-detail", args=[self.transaction.id])
        response = self.client.get(url, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test POST(create) transaction route
    def test_create_transactions(self):
        url = reverse("transaction-list")
        data = {
            "user": self.user.id,
            "amount": 100,
            "description": "test transaction",
            "date": "2023-08-27"
        }
        response = self.client.post(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 2)

    # Test PUT(update) transaction by id route
    def test_update_transaction_by_id(self):
        url = reverse("transaction-detail", args=[self.transaction.id])
        data = {
            "user": self.user.id,
            "amount": 1000,
            "description": "test transaction2",
            "date": "2023-10-10"
        }
        response = self.client.put(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the object from the database and check the updated data
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.amount, data["amount"])
        self.assertEqual(self.transaction.description, data["description"])
        self.assertEqual(self.transaction.date.strftime("%Y-%m-%d"), data["date"])

    # Test PATCH(update) transaction by id route
    def test_patch_transaction_by_id(self):
        url = reverse("transaction-detail", args=[self.transaction.id])
        data = {
            "user": self.user.id,
            "amount": 1000,
            "description": "test transaction2",
            "date": "2023-10-10"
        }
        response = self.client.patch(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the object from the database and check the updated data
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.amount, data["amount"])
        self.assertEqual(self.transaction.description, data["description"])
        self.assertEqual(self.transaction.date.strftime("%Y-%m-%d"), data["date"])

    # Test DELETE transaction by id route
    def test_delete_transaction_by_id(self):
        url = reverse("transaction-detail", args=[self.transaction.id])
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CardTransactionAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Generate the token and add it to the auth header
        refresh = RefreshToken.for_user(self.user)
        self.token_value = str(refresh.access_token)
        self.auth_header = f"Bearer {self.token_value}"

        # create card transaction associated with the user
        self.card_transaction = CardTransaction.objects.create(
            card = PaymentCard.objects.create(
                user = self.user,
                card_number = "4111111111111111",
                card_holder_name = "testuser",
                cvv = "123",
                expiry_date = "2023-08-27",
            ),
            transaction = Transaction.objects.create(
                user = self.user,
                amount = 100,
                description = "test transaction",
                date = "2023-08-27"
            )
        )

    # Test GET all card transactions route
    def test_list_card_transactions(self):
        url = reverse("cardtransaction-list")
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test GET card transaction by id route
    def test_get_card_transactions_by_id(self):
        url = reverse("cardtransaction-detail", args=[self.card_transaction.id])
        response = self.client.get(url, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test POST(create) card transaction route
    def test_create_card_transactions(self):
        url = reverse("cardtransaction-list")
        data = {
            "card": self.card_transaction.card.id,
            "transaction": self.card_transaction.transaction.id
        }
        response = self.client.post(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CardTransaction.objects.count(), 2)

    # Test PUT(update) card transaction by id route
    def test_update_card_transaction_by_id(self):
        url = reverse("cardtransaction-detail", args=[self.card_transaction.id])
        data = {
            "card": self.card_transaction.card.id,
            "transaction": self.card_transaction.transaction.id
        }
        response = self.client.put(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the object from the database and check the updated data
        self.card_transaction.refresh_from_db()
        self.assertEqual(self.card_transaction.card.id, data["card"])
        self.assertEqual(self.card_transaction.transaction.id, data["transaction"])

    # Test PATCH(update) card transaction by id route
    def test_patch_card_transaction_by_id(self):
        url = reverse("cardtransaction-detail", args=[self.card_transaction.id])
        data = {
            "card": self.card_transaction.card.id,
            "transaction": self.card_transaction.transaction.id
        }
        response = self.client.patch(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the object from the database and check the updated data
        self.card_transaction.refresh_from_db()
        self.assertEqual(self.card_transaction.card.id, data["card"])
        self.assertEqual(self.card_transaction.transaction.id, data["transaction"])

    # Test DELETE card transaction by id route
    def test_delete_card_transaction_by_id(self):
        url = reverse("cardtransaction-detail", args=[self.card_transaction.id])
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
