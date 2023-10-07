from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from cubeseed.purchase_orders.models import PurchaseOrder
from .models import FarmPlanner, OrderTracker


class FarmPlannerTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")

        # generate jwt token for the user
        refresh  = RefreshToken.for_user(self.user)
        self.token_value = str(refresh.access_token)
        self.auth_headers = f"Bearer {self.token_value}"
        # create the farm planner model
        self.farm_planner = FarmPlanner.objects.create(
            farmer=self.user,
            purchase_order = PurchaseOrder.objects.create(
                name="test purchase order",
                date_sent="2021-01-01",
                delivery_date="2021-01-01",
                delivery_venue="test venue",
                products="test products",
                price=100.00,
                buyer_name="test buyer",
                terms_and_conditions="test terms and conditions"
            ),
            order_tracker = OrderTracker.objects.create(
                purchase_order = PurchaseOrder.objects.create(
                    name="test purchase order",
                    date_sent="2021-01-01",
                    delivery_date="2021-01-01",
                    delivery_venue="test venue",
                    products="test products",
                    price=100.00,
                    buyer_name="test buyer",
                    terms_and_conditions="test terms and conditions"
                ),
                status="pending",
                description="test description"
            ),
            short_description="test description",
            order_status = "pending",
            timestamp = "2021-01-01"
            )

    #Test the Get route
    def test_get_farmplanner(self):
        url = reverse('farmplanner-list')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test GET by Id
    def test_get_specific_farmplanner(self):
        url = reverse('farmplanner-detail', args=[self.farm_planner.id])
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test POST route
    def test_create_farmplanner(self):
        url = reverse('farmplanner-list')
        data = {
            "farmer": self.user.id,
            "purchase_order": self.farm_planner.purchase_order.id,
            "short_description": "test description",
            "order_tracker": self.farm_planner.order_tracker.id,
            "order_status": "pending",
            "timestamp": "2021-01-01"
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test PUT route
    def test_update_farmplanner(self):
        url = reverse('farmplanner-detail', kwargs={'pk': self.farm_planner.pk})
        updated_data = {
            "farmer": self.user.id,
            "purchase_order": self.farm_planner.purchase_order.id,
            'short_description': 'Updated Farm Planner',
            'order_status': 'accepted',
        }
        response = self.client.put(url, updated_data, format='json', HTTP_AUTHORIZATION=self.auth_headers)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test PATCH route
    def test_patch_farmplanner(self):
        url = reverse('farmplanner-detail', kwargs={'pk': self.farm_planner.pk})
        updated_data = {
            "farmer": self.user.id,
            "purchase_order": self.farm_planner.purchase_order.id,
            'short_description': 'Updated Farm Planner',
            'order_status': 'accepted',
        }
        response = self.client.patch(url, updated_data, format='json', HTTP_AUTHORIZATION=self.auth_headers)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test delete route
    def test_delete_farmplanner(self):
        url = reverse('farmplanner-detail', kwargs={'pk': self.farm_planner.pk})
        response = self.client.delete(url, format='json', HTTP_AUTHORIZATION=self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FarmPlanner.objects.count(), 0)
