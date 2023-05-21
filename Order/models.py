from django.db import models
from Core.models import BaseModel
from Customers.models import Customer
from Product.models import Product
import jdatetime


class Order(BaseModel):
    customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.CASCADE)
    registration_date = models.DateTimeField("تاریخ ثبت", default=jdatetime.datetime.now, null=False, blank=False)
    delivery_date = models.DateField("تاریخ دریافت", null=False, blank=False)
    address = models.TextField("آدرس", null=False, blank=False)
    product = models.ManyToManyField(Product, related_name="order_product")

    class Meta:
        ordering = ["registration_date"]

    def __str__(self):
        return f"{self.customer}"
