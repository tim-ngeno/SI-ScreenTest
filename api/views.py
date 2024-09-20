# from django.shortcuts import render
import os
import africastalking
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from django.contrib.auth import login
from django.contrib.auth.models import User
from mozilla_django_oidc.views import OIDCAuthenticationCallbackView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from dotenv import load_dotenv

load_dotenv()


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_class = [IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_class = [IsAuthenticated]

    def perform_create(self, serializer):
        order = serializer.save()
        self.send_sms_alert(order)

    def send_sms_alert(self, order):
        username = "sandbox"
        apikey = os.getenv("SMS_APIKEY")

        africastalking.initialize(username, apikey)

        sms = africastalking.SMS

        recipients = ["+254106526816"]
        message = f"Hi, {order.customer.name}, you have successfully placed an order for {order.item} amounting to {order.amount}."

        try:
            res = sms.send(message, recipients)
            print(res)
        except Exception as e:
            print(f"Error sending SMS: {e}")


# @login_required
# def get_customers(request):
#     customers = Customer.objects.all()
#     customer = Customer.objects.filter(code=request.user.email)
#     context = {
#         "customer": customer,
#         "customers": customers,
#     }
#     if customer:
#         print("yeah, we got one!")
#         print(customer)
#         print(customer.name)
#         print(customer.code)
#     return render(request, "api/customers.html", context)


# @login_required
# def get_orders(request):
#     orders = Order.objects.all()
#     return render(request, "api/orders.html", {"orders": orders})


class CustomOIDCCallback(OIDCAuthenticationCallbackView):
    def get(self, request, *args, **kwargs):
        user_info = request.oidc.userinfo()
        email = user_info.get("email")

        user, created = User.objects.get_or_create(
            username=email, defaults={"email": email}
        )
        if created:
            print("success!")
        login(request, user)

        # Register the customer as a user
        customer, created = Customer.objects.get_or_create(
            code=email,
            defaults={
                "name": user_info.get("name", f"{email.split('@')[0]}"),
                "phone_number": "",
            },
        )
        print(customer.code)
        if created:
            return super().get(request, *args, **kwargs)
