from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ProcessStorage, DispatchedStorage


# Create your tests here.
class ProcessStorageAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="<PASSWORD>")

        # generate the token and add it to the auth header
        refresh = RefreshToken.for_user(self.user)
        self.token_value = str(refresh.access_token)
        self.auth_header = f"Bearer {self.token_value}"

        # create the process storage object
        self.process_storage = ProcessStorage.objects.create(
            location="test location",
            services="test services",
            paymentdetails="test payment details"
        )

    # POST route
    def test_create_process_storage(self):

        url = reverse("processstorage-list")
        data = {
            "location": "new location",
            "services": "new services",
            "paymentdetails": "new payment details"
        }

        response = self.client.post(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProcessStorage.objects.count(), 2)

    # GET route
    def test_get_process_storage(self):
        process_storage = self.process_storage

        url = reverse("processstorage-detail", kwargs={"pk": process_storage.id})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check if the response data is the same as the created process storage
        self.assertEqual(response.data["location"], process_storage.location)
        self.assertEqual(response.data["services"], process_storage.services)
        self.assertEqual(response.data["paymentdetails"], process_storage.paymentdetails)

    # PUT route
    def test_update_process_storage(self):
        process_storage = self.process_storage

        url = reverse("processstorage-detail", kwargs={"pk": process_storage.id})
        updated_data = {
            "location": "new location",
            "services": "new services",
            "paymentdetails": "new payment details"
        }

        response = self.client.put(url, updated_data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # refresh the process storage object from db
        process_storage.refresh_from_db()

        # check if the process storage object is updated
        self.assertEqual(process_storage.location, updated_data["location"])
        self.assertEqual(process_storage.services, updated_data["services"])
        self.assertEqual(process_storage.paymentdetails, updated_data["paymentdetails"])

    # PATCH route
    def test_partial_update_process_storage(self):
        process_storage = self.process_storage

        url = reverse("processstorage-detail", kwargs={"pk": process_storage.id})
        updated_data = {
            "location": "new location",
        }
        response = self.client.patch(url, updated_data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # refresh the process storage object from db
        process_storage.refresh_from_db()

        # check if the process storage object is updated
        self.assertEqual(process_storage.location, updated_data["location"])
        self.assertEqual(process_storage.services, process_storage.services)
        self.assertEqual(process_storage.paymentdetails, process_storage.paymentdetails)

    # DELETE route
    def test_delete_process_storage(self):
        process_storage = self.process_storage

        url = reverse("processstorage-detail", kwargs={"pk": process_storage.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ProcessStorage.objects.count(), 0)


class DispatchedStorageAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="<PASSWORD>")

        # generate the token and add it to the auth header
        refresh = RefreshToken.for_user(self.user)
        self.token_value = str(refresh.access_token)
        self.auth_header = f"Bearer {self.token_value}"

        # create the process storage object
        self.dispatched_storage = DispatchedStorage.objects.create(
            driver_name = "test driver name",
            vehical_id = "test vehical id",
            farmer = "test farmer",
            farmer_location = "test farmer location",
            invoice_id = "test invoice_id",
            receipt_id = "test receipt_id",
            waybill_id = "test waybill_id",
            grn_id = "test grn_id",
            goods_received_note = "test goods_received"
        )

    # POST route

    def test_create_dispatched_storage(self):

        url = reverse("dispatchedstorage-list")
        data = {
            "driver_name": "new driver name",
            "vehical_id": "new vehical id",
            "farmer": "new farmer",
            "farmer_location": "new farmer location",
            "invoice_id": "new invoice_id",
            "receipt_id": "new receipt_id",
            "waybill_id": "new waybill_id",
            "grn_id": "new grn_id",
            "goods_received_note": "new goods_received"
        }
        response = self.client.post(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DispatchedStorage.objects.count(), 1)


    # GET route
    def test_get_dispatched_storage(self):
        dispatched_storage = self.dispatched_storage

        url = reverse("dispatchedstorage-detail", kwargs={"pk": dispatched_storage.id})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["driver_name"], dispatched_storage.driver_name)
        self.assertEqual(response.data["vehical_id"], dispatched_storage.vehical_id)
        self.assertEqual(response.data["farmer"], dispatched_storage.farmer)
        self.assertEqual(response.data["farmer_location"], dispatched_storage.farmer_location)
        self.assertEqual(response.data["invoice_id"], dispatched_storage.invoice_id)
        self.assertEqual(response.data["receipt_id"], dispatched_storage.receipt_id)
        self.assertEqual(response.data["waybill_id"], dispatched_storage.waybill_id)
        self.assertEqual(response.data["grn_id"], dispatched_storage.grn_id)
        self.assertEqual(response.data["goods_received_note"], dispatched_storage.goods_received_note)

    # PUT route
    def test_update_dispatched_storage(self):
        dispatched_storage = self.dispatched_storage

        url = reverse("dispatchedstorage-detail", kwargs={"pk": self.dispatched_storage.id})
        updated_data = {
            "driver_name": "new driver name",
            "vehical_id": "new vehical id",
            "farmer": "new farmer",
            "farmer_location": "new farmer location",
            "invoice_id": "new invoice_id",
            "receipt_id": "new receipt_id",
            "waybill_id": "new waybill_id",
            "grn_id": "new grn_id",
            "goods_received_note": "new goods_received"
        }

        response = self.client.put(url, updated_data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.dispatched_storage.refresh_from_db()
        self.assertEqual(self.dispatched_storage.driver_name, updated_data["driver_name"])
        self.assertEqual(self.dispatched_storage.vehical_id, updated_data["vehical_id"])
        self.assertEqual(self.dispatched_storage.farmer, updated_data["farmer"])
        self.assertEqual(self.dispatched_storage.farmer_location, updated_data["farmer_location"])
        self.assertEqual(self.dispatched_storage.invoice_id, updated_data["invoice_id"])
        self.assertEqual(self.dispatched_storage.receipt_id, updated_data["receipt_id"])
        self.assertEqual(self.dispatched_storage.waybill_id, updated_data["waybill_id"])
        self.assertEqual(self.dispatched_storage.grn_id, updated_data["grn_id"])
        self.assertEqual(self.dispatched_storage.goods_received_note, updated_data["goods_received_note"])


    # PATCH route
    def test_partial_update_dispatched_storage(self):
        dispatched_storage = self.dispatched_storage

        url = reverse("dispatchedstorage-detail", kwargs={"pk": dispatched_storage.id})
        updated_data = {
            "driver_name": "new driver name",
            "vehical_id": "new vehical id",
            "farmer": "new farmer",
            "farmer_location": "new farmer location",
            "invoice_id": "new invoice_id",
            "receipt_id": "new receipt_id",
            "waybill_id": "new waybill_id",
            "grn_id": "new grn_id",
            "goods_received_note": "new goods_received"
        }

        response = self.client.patch(url, updated_data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.dispatched_storage.refresh_from_db()

        self.assertEqual(self.dispatched_storage.driver_name, updated_data["driver_name"])
        self.assertEqual(self.dispatched_storage.vehical_id, updated_data["vehical_id"])
        self.assertEqual(self.dispatched_storage.farmer, updated_data["farmer"])
        self.assertEqual(self.dispatched_storage.farmer_location, updated_data["farmer_location"])
        self.assertEqual(self.dispatched_storage.invoice_id, updated_data["invoice_id"])
        self.assertEqual(self.dispatched_storage.receipt_id, updated_data["receipt_id"])
        self.assertEqual(self.dispatched_storage.waybill_id, updated_data["waybill_id"])
        self.assertEqual(self.dispatched_storage.grn_id, updated_data["grn_id"])
        self.assertEqual(self.dispatched_storage.goods_received_note, updated_data["goods_received_note"])

    # DELETE route
    def test_delete_dispatched_storage(self):
        dispatched_storage = self.dispatched_storage

        url = reverse("dispatchedstorage-detail", kwargs={"pk": dispatched_storage.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DispatchedStorage.objects.count(), 0)
