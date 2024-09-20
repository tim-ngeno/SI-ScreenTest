from django.db import models


class Customer(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, null=True)

    def __str__(self):
        return f"{self.name} - {self.code}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item} ordered by {self.customer} at {self.time}"
