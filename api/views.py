import os
import africastalking
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
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
        username = os.getenv("SMS_USERNAME")
        apikey = os.getenv("SMS_APIKEY")

        africastalking.initialize(username, apikey)

        sms = africastalking.SMS

        recipients = [f"+{phone_number}"]
        customer = order.customer.name.strip()
        item = order.item.strip()
        amount = order.amount
        message = f"Hi, {customer}. You have successfully made an order for {item} amounting to Kshs. {amount}"
        print(repr(message))

        try:
            res = sms.send(message, recipients)
            print(res)
        except Exception as e:
            print(f"Error sending SMS: {e}")
