# from django.urls import reverse
# from django.contrib.auth.models import User
# from rest_framework.test import APITestCase, APIClient
# from rest_framework.authtoken.models import Token
# from rest_framework_simplejwt.tokens import AccessToken
# from rest_framework import status
# from .models import Customer, Order
# from unittest.mock import patch


# class CustomerTestCase(APITestCase):
#     """Test case for Customer model operations"""

#     def setUp(self):
#         """Initializes a test customer and sets the url for customer endpoints."""
#         # self.customer = Customer.objects.create(
#         #     name="Test Customer",
#         #     code="test@example.com",
#         # )
#         # self.url = reverse("customer-list")
#         # self.client = APIClient()
#         # token = AccessToken.for_user(self.customer)
#         # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
#         self.url = reverse("customer-list")

#     @patch("core.login_middleware.LoginRequiredMiddleware.__call__")
#     def test_list_customers(self, mock_middleware):
#         """Tests retrieving a list of customers via the api"""

#         def mock_middleware_call(request):
#             user = User.objects.create_user(
#                 username="testuser123", password="testpassword"
#             )
#             request.user = user
#             return self.client.get(self.url)

#         mock_middleware.side_effect = mock_middleware_call

#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]["name"], self.customer.name)


# class OrderTestCase(APITestCase):
#     """Test case for order moodel operations"""
#     def setUp(self):
#         """Initializes a test customer and tests url for order endpoints"""
#         self.customer = Customer.objects.create(
#             name="Test Customer",
#             code="121-ASDAF242",
#         )
#         self.url = reverse("order-list")

# def test_create_order(self):
#     """Tests creation of orders"""
#     data = {
#         "customer": self.customer.id,
#         "item": "Test Item",
#         "amount": 100.93,
#     }
#     response = self.client.post(self.url, data, format="json")
#     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#     self.assertEqual(Order.objects.count(), 1)
#     self.assertEqual(Order.objects.first().item, "Test Item")
