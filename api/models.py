from django.db import models


class Customer(models.Model):
    """Creates a customer in the system

    Attribbutes:
        name (str): The name of the customer
        code (str): A unique identifier for the customer
        phone_number (str): The customer's phone number
    """

    name = models.CharField(max_length=120)
    code = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, null=True)

    def __str__(self):
        """Returns a string representation of the customer"""
        return f"{self.name} - {self.code}"


class Order(models.Model):
    """Represents an order placed by a customer

    Attributes:
        customer (Customer): The customer placing the order
        item (str): The name of the item ordered
        amount (float): The total amount of the order
        time (datetime): The time when the order was placed"""

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True).strftime("dd-mm-YY")

    def __str__(self):
        """Returns a string representation of the order"""
        return f"{self.item} ordered by {self.customer} at {self.time}"
