from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Invoice, Waybill, Receipt
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from cubeseed.userprofile.models import UserProfile
from cubeseed.address.models import Address
from unittest.mock import Mock
from unittest.mock import patch

# Create a Mock of the resolve_location method found
# in the Address model.
# This prevents the geocode function from being 
# called multiple times.
mock_resolve_location = Mock()

def side_effect(address):
    class Location:
        def __init__(self, latitude, longitude):
            self.longitude = longitude
            self.latitude = latitude
    if address == "979 Saka Jojo Street, Victoria, Lagos, ":
        location = Location(6.4275875, 3.4126698)
        return location
    elif address == "2 Walter Carrington Crescent, Victoria Island, Lagos, ":
        location = Location(6.44069015, 3.4066570357293076)
        return location
    elif address == "1075 Diplomatic Drive, Central District Area, Abuja, 900103":
        location = Location(9.0403859, 7.4768889)
        return location
    else:
        return None

class InvoiceAPITestCase(APITestCase):
    @patch.object(Address, "resolve_location", side_effect=side_effect)
    def setUp(self, mock_resolve_location):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Generate the token and add it to the auth header
        refresh = RefreshToken.for_user(self.user)
        self.token_value = str(refresh.access_token)
        self.auth_header = f"Bearer {self.token_value}"

        self.address = Address.objects.create(
            address="979 Saka Jojo Street",
            locality="Victoria",
            administrative_area="Lagos",
            country="NG",
            postal_code="12345",
            osm_checked=True,
            osm_latitude=0.0,
            osm_longitude=0.0,
            local_government_area="Eti Osa",
            updated_at="2023-08-27T12:41:06.021393Z",
            created_at="2023-08-27T12:41:06.021348Z"

        )

        # create end user
        self.end_user = UserProfile.objects.create(
            full_name="testuserprofile",
            phone_number="1234567890",
            address=self.address,
            about_me="testing-0987689",
            user=self.user,
            created_at="2023-08-27T12:41:06.021348Z",
            updated_at="2023-08-27T12:41:06.021393Z"
        )

        # Create an Invoice object for testing
        self.invoice = Invoice.objects.create(
            payment_due_date="2023-08-27",
            notes="testing-0987689",
            signature="",
            sent="False",
            invoice_date="2023-08-27T12:41:06.021393Z",
            sent_by=self.user,
            delivered_to=self.end_user,
            service="testing",
            service_details="testing",
            quantity="1",
            weight="1.0",
            unit_price="1.0",
            total_price="1.0"
        )
        # Create a 100x100 white image; signature image
        image = Image.new('RGB', (100, 100), (255, 255, 255))

        # Save the image to a BytesIO object
        image_io = io.BytesIO()
        image.save(image_io, format='PNG')
        image_io.seek(0)  # Reset the stream position to the beginning

        # Create a SimpleUploadedFile using the BytesIO data
        self.image_file = SimpleUploadedFile("test_image.png", image_io.read(), content_type="image/png")

    # Testing the GET all the invoices route
    def test_list_invoice(self):
        url = reverse("invoice-list")
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing Get invoice by id route
    def test_get_invoice_by_id(self):
        url = reverse("invoice-detail", args=[self.invoice.id])
        response = self.client.get(url, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing the POST(create) route
    def test_create_invoice(self):
        url = reverse("invoice-list")
        data = {
            "payment_due_date": "2023-08-27",
            "notes": "testing-0987689",
            "signature": self.image_file,
            "sent_by": self.user.id,
            "delivered_to": self.end_user.id,
            "service": "testing",
            "service_details": "testing",
            "quantity": "1",
            "weight": "1.0",
            "unit_price": "1.0",
            "total_price": "1.0"
        }
        response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Testing the PUT(update) route
    def test_update_invoice(self):
        url = reverse("invoice-detail", args=[self.invoice.id])
        data = {
            "payment_due_date": "2023-08-27",
            "notes": "testing-0987689",
            "signature": self.image_file,
            "sent_by": self.user.id,
            "delivered_to": self.end_user.id,
            "service": "testing",
            "service_details": "testing",
            "quantity": "1",
            "weight": "1.0",
            "unit_price": "1.0",
            "total_price": "1.0"
        }
        response = self.client.put(url, data, format="multipart", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #test the patch route
    def test_patch_invoice(self):
        url = reverse("invoice-detail", args=[self.invoice.id])
        data = {
            "payment_due_date": "2023-08-27",
            "notes": "testing-0987689",
            "sent": "False",
            "date": "2023-08-27"
        }
        response = self.client.patch(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing the DELETE route
    def test_delete_invoice(self):
        url = reverse("invoice-detail", args=[self.invoice.id])
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class WaybillAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Generate the token and add it to the auth header
        refresh = RefreshToken.for_user(self.user)
        self.token_value = str(refresh.access_token)
        self.auth_header = f"Bearer {self.token_value}"

        # create a Waybill object for testing
        self.waybill = Waybill.objects.create(
            delivery_date="2023-08-27",
            delivery_guy_first_name="testing",
            delivery_guy_last_name="testing",
            vehicle_name="testing",
            vehicle_model="testing",
            vehicle_license_number="testing",
            insurer_name="testing",
            policy_number="testing",
            delivery_notes="testing",
            signature="null",
            sent="False",
            date="2023-08-27T12:41:06.021393Z"
        )

        # Create a 100x100 white image; signature image
        image = Image.new('RGB', (100, 100), (255, 255, 255))

        # Save the image to a BytesIO object
        image_io = io.BytesIO()
        image.save(image_io, format='PNG')
        image_io.seek(0)  # Reset the stream position to the beginning

        # Create a SimpleUploadedFile using the BytesIO data
        self.image_file = SimpleUploadedFile("test_image.png", image_io.read(), content_type="image/png")

    # Testing the GET all the waybills route
    def test_list_waybill(self):
        url = reverse("waybill-list")
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing Get waybill by id route
    def test_get_waybill_by_id(self):
        url = reverse("waybill-detail", args=[self.waybill.id])
        response = self.client.get(url, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing the POST(create) route
    def test_create_waybill(self):
        url = reverse("waybill-list")
        data = {
            "delivery_date": "2023-08-27",
            "delivery_guy_first_name": "testing",
            "delivery_guy_last_name": "testing",
            "vehicle_name": "testing",
            "vehicle_model": "testing",
            "vehicle_license_number": "testing",
            "insurer_name": "testing",
            "policy_number": "testing",
            "delivery_notes": "testing",
            "signature": self.image_file,
            "sent": "False",
            "date": "2023-08-27T12:41:06.021393Z"
        }
        response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Testing the PUT(update) route
    def test_update_waybill(self):
        url = reverse("waybill-detail", args=[self.waybill.id])
        data = {
            "delivery_date": "2023-08-27",
            "delivery_guy_first_name": "testing",
            "delivery_guy_last_name": "testing",
            "vehicle_name": "testing",
            "vehicle_model": "testing",
            "vehicle_license_number": "testing",
            "insurer_name": "testing",
            "policy_number": "testing2",
            "delivery_notes": "testing2",
            "signature": self.image_file,
            "sent": "False",
            "date": "2023-08-27T12:41:06.021393Z"
        }
        response = self.client.put(url, data, format="multipart", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Waybill.objects.get().policy_number, "testing2")
        self.assertEqual(Waybill.objects.get().delivery_notes, "testing2")

    #test the patch route
    def test_patch_waybill(self):
        url = reverse("waybill-detail", args=[self.waybill.id])
        data = {
            "delivery_date": "2023-08-27",
            "delivery_guy_first_name": "testing",
            "delivery_guy_last_name": "testing",
            "vehicle_name": "testing",
            "vehicle_model": "testing",
            "vehicle_license_number": "testing",
            "insurer_name": "testing",
            "policy_number": "testing3",
            "delivery_notes": "testing3",
            "signature": self.image_file,
            "sent": "False",
            "date": "2023-08-27T12:41:06.021393Z"
        }
        response = self.client.patch(url, data, format="multipart", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Waybill.objects.get().policy_number, "testing3")
        self.assertEqual(Waybill.objects.get().delivery_notes, "testing3")

    # Testing the DELETE route
    def test_delete_waybill(self):
        url = reverse("waybill-detail", args=[self.waybill.id])
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ReceiptAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Generate the token and add it to the auth header
        refresh = RefreshToken.for_user(self.user)
        self.token_value = str(refresh.access_token)
        self.auth_header = f"Bearer {self.token_value}"

                # Create a 100x100 white image; signature image
        image = Image.new('RGB', (100, 100), (255, 255, 255))

        # create a Receipt object for testing
        self.receipt = Receipt.objects.create(
            amount="1000.00",
            payment_date="2023-08-27",
            payment_method="testing",
            payment_notes="testing",
            date="2023-08-27",
            signature="",
            sent="False",
        )
        # Create a 100x100 white image; signature image
        image = Image.new('RGB', (100, 100), (255, 255, 255))

        # Save the image to a BytesIO object
        image_io = io.BytesIO()
        image.save(image_io, format='PNG')
        image_io.seek(0)  # Reset the stream position to the beginning

        # Create a SimpleUploadedFile using the BytesIO data
        self.image_file = SimpleUploadedFile("test_image.png", image_io.read(), content_type="image/png")

    # Testing the GET all the receipts route
    def test_list_receipt(self):
        url = reverse("receipt-list")
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing Get receipt by id route
    def test_get_receipt_by_id(self):
        url = reverse("receipt-detail", args=[self.receipt.id])
        response = self.client.get(url, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing the POST(create) route
    def test_create_receipt(self):
        url = reverse("receipt-list")
        data = {
            "amount": "1000.00",
            "payment_date": "2023-08-27",
            "payment_method": "testing",
            "payment_notes": "testing",
            "date": "2023-08-27",
            "signature": self.image_file,
            "sent": "False",
        }
        response = self.client.post(url, data, format="multipart", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Testing the PUT(update) route
    def test_update_receipt(self):
        url = reverse("receipt-detail", args=[self.receipt.id])
        data = {
            "amount": "1000.00",
            "payment_date": "2023-08-28",
            "payment_method": "testing4",
            "payment_notes": "testing4",
            "date": "2023-08-2",
            "signature": self.image_file,
            "sent": "False",
        }
        response = self.client.put(url, data, format="multipart", HTTP_AUTHORIZATION=self.auth_header)

        # refresh db
        self.receipt.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Receipt.objects.get().payment_method, "testing4")
        self.assertEqual(Receipt.objects.get().payment_notes, "testing4")
        self.assertEqual(Receipt.objects.get().payment_date.strftime("%Y-%m-%d"), "2023-08-28")

    # Test patch route
    def test_patch_receipt(self):
        url = reverse('receipt-detail', args=[self.receipt.id])
        data = {
            "amount": "19.00",
            "payment_date": "2023-09-07"
        }
        response = self.client.patch(url, data, format="multipart", HTTP_AUTHORIZATION=self.auth_header)

        # refresh db
        self.receipt.refresh_from_db()

        # check the updated vales
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(Receipt.objects.get().amount), "19.00")
        self.assertEqual(Receipt.objects.get().payment_date.strftime("%Y-%m-%d"), "2023-09-07")

    # Test the DELETE route
    def test_delete_reciept(self):
        url = reverse('receipt-detail', args=[self.receipt.id])
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
