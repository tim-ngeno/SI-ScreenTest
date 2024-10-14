from rest_framework import serializers
from .models import Customer, Order


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer class for the Customer model"""

    class Meta:
        model = Customer
        fields = ["id", "name", "code", "phone_number"]


class OrderSerializer(serializers.ModelSerializer):
    """Serializer class for the Order model"""

    class Meta:
        model = Order
        fields = ["id", "customer", "item", "amount", "time"]
