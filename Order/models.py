from django.db import models
from Core.models import BaseModel
from Customers.models import Customer
from django.utils import timezone


class Order(BaseModel):
    customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.CASCADE)
    registration_date = models.DateTimeField("Registration Date", auto_now_add=timezone.now, null=False, blank=False)
    delivery_date = models.DateField("Delivery Date", null=False, blank=False)
    address = models.TextField("Address", null=False, blank=False)

    class Meta:
        ordering = ["registration_date"]

    def __str__(self):
        return f"{self.customer}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.DO_NOTHING)
    product = models.ForeignKey("Product", null=False, blank=False, on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True
