from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from .models import PurchaseOrder, OpenedPurchaseOrder



class PurchaseOrderTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # generate the token and add it to the auth header
        refresh = RefreshToken.for_user(self.user)
        self.token_value = str(refresh.access_token)
        self.auth_header = f"Bearer {self.token_value}"
        self.purchase_order = PurchaseOrder.objects.create(
            name="test purchase order",
            date_sent="2021-01-01",
            delivery_date="2021-01-01",
            delivery_venue="test venue",
            products="test products",
            price=100.00,
            buyer_name="test buyer",
            terms_and_conditions="test terms and conditions"
        )

    # POST route
    def test_create_purchase_order(self):
        url = reverse("purchaseorder-list")
        data = {
            "name": "new purchase order",
            "date_sent": "2021-02-02",
            "delivery_date": "2021-02-02",
            "delivery_venue": "new venue",
            "products": "new products",
            "price": 200.00,
            "buyer_name": "new buyer",
            "terms_and_conditions": "new terms and conditions"
        }

        response = self.client.post(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)

    # GET route
    def test_get_purchase_order(self):
        purchase_order = self.purchase_order

        url = reverse("purchaseorder-detail", kwargs={"pk": purchase_order.id})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # convert the price to string to compare with the response data
        expected_price = "{:.2f}".format(purchase_order.price)

        # chack if the response data is the same as the created purchase order
        self.assertEqual(response.data["name"], purchase_order.name)
        self.assertEqual(response.data["date_sent"], purchase_order.date_sent)
        self.assertEqual(response.data["delivery_date"], purchase_order.delivery_date)
        self.assertEqual(response.data["delivery_venue"], purchase_order.delivery_venue)
        self.assertEqual(response.data["products"], purchase_order.products)
        self.assertEqual(response.data["price"], expected_price)
        self.assertEqual(response.data["buyer_name"], purchase_order.buyer_name)
        self.assertEqual(response.data["terms_and_conditions"], purchase_order.terms_and_conditions)

    # PUT route
    def test_update_purchase_order(self):
        purchase_order = self.purchase_order

        url = reverse("purchaseorder-detail", kwargs={"pk": purchase_order.id})
        updated_data = {
            "name": "Updated Order",
            "date_sent": "2021-10-10",
            "delivery_date": "2021-10-10",
            "delivery_venue": "Updated Venue",
            "products": "Updated Products",
            "price": 200.00,
            "buyer_name": "Updated Buyer",
            "terms_and_conditions": "Updated Terms and Conditions"
            }

        response = self.client.put(url, updated_data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # refresh the purchase order object from db
        purchase_order.refresh_from_db()

        # check if the purchase order object is updated
        self.assertEqual(purchase_order.name, updated_data["name"])
        self.assertEqual(str(purchase_order.date_sent), updated_data["date_sent"])
        self.assertEqual(purchase_order.delivery_venue, updated_data["delivery_venue"])
        self.assertEqual(str(purchase_order.delivery_date), updated_data["delivery_date"])
        self.assertEqual(purchase_order.products, updated_data["products"])
        self.assertEqual(purchase_order.price, updated_data["price"])
        self.assertEqual(purchase_order.buyer_name, updated_data["buyer_name"])
        self.assertEqual(purchase_order.terms_and_conditions, updated_data["terms_and_conditions"])

    # PATCH route
    def test_partial_update_purchase_order(self):
        purchase_order = self.purchase_order

        url = reverse("purchaseorder-detail", kwargs={"pk": purchase_order.id})
        updated_data = {
            "name": "Updated Order",
            "delivery_venue": "Updated Venue",
            "price": 200.00,
        }

        response = self.client.patch(url, updated_data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the db
        purchase_order.refresh_from_db()

        # confirm the purchase order is updated properly
        self.assertEqual(purchase_order.name, updated_data["name"])
        self.assertEqual(purchase_order.delivery_venue, updated_data["delivery_venue"])
        self.assertEqual(purchase_order.price, updated_data["price"])

    # DELETE route
    def test_delete_purchase_order(self):
        purchase_order = self.purchase_order

        url = reverse("purchaseorder-detail", kwargs={"pk": purchase_order.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)


class OpenedPurchaseOrderTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # generate the token and add it to the auth header
        refresh = RefreshToken.for_user(self.user)
        self.token_value = str(refresh.access_token)
        self.auth_header = f"Bearer {self.token_value}"

        # create the purchase order object
        self.purchase_order = PurchaseOrder.objects.create(
            name="test purchase order",
            date_sent="2021-01-01",
            delivery_date="2021-01-01",
            delivery_venue="test venue",
            products="test products",
            price=100.00,
            buyer_name="test buyer",
            terms_and_conditions="test terms and conditions"
        )

    # POST route
    def test_create_opened_purchase_order(self):

        url = reverse("openedpurchaseorder-list")
        data = {
            "purchase_order": self.purchase_order.id,
            "farmer": self.user.id
        }

        response = self.client.post(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OpenedPurchaseOrder.objects.count(), 1)

    # GET route
    def test_get_opened_purchase_order(self):
        opened_purchase_order = OpenedPurchaseOrder.objects.create(
            purchase_order=self.purchase_order,
            farmer=self.user
        )

        url = reverse("openedpurchaseorder-detail", kwargs={"pk": opened_purchase_order.id})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check if the response data is the same as the created purchase order
        self.assertEqual(response.data["purchase_order"], opened_purchase_order.purchase_order.id)
        self.assertEqual(response.data["farmer"], opened_purchase_order.farmer.id)

    # PUT route
    def test_update_opened_purchase_order(self):
        opened_purchase_order = OpenedPurchaseOrder.objects.create(
            purchase_order=self.purchase_order,
            farmer=self.user
        )

        url = reverse("openedpurchaseorder-detail", kwargs={"pk": opened_purchase_order.id})
        updated_data = {
            "purchase_order": self.purchase_order.id,
            "farmer": self.user.id
        }

        response = self.client.put(url, updated_data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # refresh the purchase order object from db
        opened_purchase_order.refresh_from_db()

        # check if the purchase order object is updated
        self.assertEqual(opened_purchase_order.purchase_order.id, updated_data["purchase_order"])
        self.assertEqual(opened_purchase_order.farmer.id, updated_data["farmer"])

    # PATCH route
    def test_partial_update_opened_purchase_order(self):
        opened_purchase_order = OpenedPurchaseOrder.objects.create(
            purchase_order=self.purchase_order,
            farmer=self.user
        )

        url = reverse("openedpurchaseorder-detail", kwargs={"pk": opened_purchase_order.id})
        updated_data = {
            "purchase_order": self.purchase_order.id,
        }

        response = self.client.patch(url, updated_data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # refresh the purchase order object from db
        opened_purchase_order.refresh_from_db()

        # check if the purchase order object is updated
        self.assertEqual(opened_purchase_order.purchase_order.id, updated_data["purchase_order"])

    # DELETE route
    def test_delete_opened_purchase_order(self):
        opened_purchase_order = OpenedPurchaseOrder.objects.create(
            purchase_order=self.purchase_order,
            farmer=self.user
        )

        url = reverse("openedpurchaseorder-detail", kwargs={"pk": opened_purchase_order.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OpenedPurchaseOrder.objects.count(), 0)
