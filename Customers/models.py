from django.db import models
from Core.models import BaseModel, User


class Customer(User, BaseModel):
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.get_full_name}"


class Address(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    state = models.CharField("State", max_length=75, null=False, blank=False)
    city = models.CharField("City", max_length=100, null=False, blank=False)
    full_address = models.TextField("Full Address", null=False, blank=False)
    postal_code = models.SmallIntegerField("Postal Code", null=False, blank=False)
