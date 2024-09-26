from django.shortcuts import render
import os
import africastalking
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from mozilla_django_oidc.views import OIDCAuthenticationCallbackView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from dotenv import load_dotenv

load_dotenv()


class CustomerViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing customer instances"""

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_class = [IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing order instances"""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_class = [IsAuthenticated]

    def perform_create(self, serializer):
        """Creates a new order and sends an SMS alert"""
        order = serializer.save()
        self.send_sms_alert(order)

    def send_sms_alert(self, order):
        """Sends an SMS alert to the customer upon successful order
        placement

        Args:
            order (Order): The order object for which the SMS is sent
        """
        phone_number = order.customer.phone_number
        print(phone_number)

        # Initialize AfricasTalking SMS gateway
        username = "sandbox"
        apikey = os.getenv("SMS_APIKEY")

        africastalking.initialize(username, apikey)

        sms = africastalking.SMS

        recipients = [f"+{phone_number}"]
        message = f"Hi, {order.customer.name}, you have successfully placed an order for {order.item} amounting to {order.amount}."

        try:
            res = sms.send(message, recipients)
            print(res)
        except Exception as e:
            print(f"Error sending SMS: {e}")


# class CustomOIDCCallback(OIDCAuthenticationCallbackView):
#     def get(self, request, *args, **kwargs):
#         user_info = request.oidc.userinfo()
#         email = user_info.get("email")

#         user, created = User.objects.get_or_create(
#             username=email, defaults={"email": email}
#         )
#         if created:
#             print("success!")
#         login(request, user)

#         # Register the customer as a user
#         customer, created = Customer.objects.get_or_create(
#             code=email,
#             defaults={
#                 "name": user_info.get("name", f"{email.split('@')[0]}"),
#                 "phone_number": "",
#             },
#         )
#         print(customer.code)
#         if created:
#             return super().get(request, *args, **kwargs)
