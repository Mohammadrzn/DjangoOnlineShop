from django.db import models
from core.models import BaseModel
from customers.models import Customer
from product.models import Product


class Order(BaseModel):
    customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.CASCADE)
    registration_date = models.DateTimeField("تاریخ ثبت", auto_now_add=True, null=False, blank=False)
    delivery_date = models.DateField("تاریخ دریافت", null=False, blank=False)
    address = models.TextField("آدرس", null=False, blank=False)
    status = models.BooleanField("وضعیت سفارش", default=False)
    product = models.ManyToManyField(Product, related_name="order_product")

    class Meta:
        ordering = ["registration_date"]
        verbose_name_plural = "سفارش ها"

    def __str__(self):
        return f"{self.customer}"


class OrderItems(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', verbose_name="اقلام سفارش", on_delete=models.CASCADE)
    count = models.IntegerField("تعداد")
    product = models.ForeignKey(Product, verbose_name="محصول", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "اقلام سفارش"
        verbose_name_plural = 'اقلام فاکتور'

    def __str__(self) -> str:
        return f"{self.Product.name}"

    def item_cost(self):
        return self.count * self.Product.price

    def item_discount(self):
        return self.Product.total_discount * self.count
