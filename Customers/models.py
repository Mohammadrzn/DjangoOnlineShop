from django.db import models
from Core.models import User, BaseModel


class Customer(User, BaseModel):
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class Address(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    state = models.CharField("State", max_length=75, null=False, blank=False)
    city = models.CharField("City", max_length=100, null=False, blank=False)
    full_address = models.TextField("Full Address", null=False, blank=False)
    postal_code = models.CharField("Postal Code", max_length=10)
