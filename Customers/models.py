from django.db import models
from Core.models import BaseModel, User


class Customer(User, BaseModel):
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Address(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    state = models.CharField("State", max_length=75, null=False, blank=False)
    city = models.CharField("City", max_length=100, null=False, blank=False)
    full_address = models.TextField("Full Address", null=False, blank=False)
    postal_code = models.SmallIntegerField("Postal Code", null=False, blank=False)
    is_deleted = None

    class Meta:
        verbose_name = "Address"

    def __str__(self):
        return f"{self.customer_id}"
