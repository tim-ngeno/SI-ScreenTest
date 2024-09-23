from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Customer, Order


class CustomerTestCase(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Test Customer",
            code="test@example.com",
        )
        self.url = reverse("customer-list")

    def test_list_customers(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.customer.name)


class OrderTestCase(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Test Customer",
            code="121-ASDAF242",
        )
        self.url = reverse("order-list")

    def test_create_order(self):
        data = {
            "customer": self.customer.id,
            "item": "Test Item",
            "amount": 100.93,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().item, "Test Item")
