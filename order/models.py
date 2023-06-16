from django.db import models
from core.models import BaseModel
from customers.models import Customer
from product.models import Product


class Order(BaseModel):
    customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.CASCADE)
    registration_date = models.DateTimeField("تاریخ ثبت", auto_now_add=True, null=False, blank=False)
    delivery_date = models.DateField("تاریخ دریافت", null=True, blank=True)
    address = models.TextField("آدرس", null=False, blank=False)
    status = models.BooleanField("وضعیت سفارش", default=False)
    product = models.ManyToManyField(Product, related_name="order_product")

    class Meta:
        ordering = ["registration_date"]
        verbose_name_plural = "سفارش ها"

    @property
    def total_price(self):
        order_items = self.order_items.all()
        total = sum(item.item_cost for item in order_items)
        return total

    @property
    def total_discount(self):
        order_items = self.order_items.all()
        total = sum(item.item_discount for item in order_items)
        return total

    def total_payment(self):
        return self.total_price - self.total_discount

    def __str__(self):
        return f"{self.customer}"


class Carts(BaseModel):
    customer = models.ForeignKey(Customer, verbose_name="مشتری", on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='CartItems', verbose_name="محصول")

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد خرید"

    def __str__(self) -> str:
        return f"{self.customer.get_full_name}سبد "


class CartItems(models.Model):
    cart = models.ForeignKey(Carts, related_name='order_item', verbose_name="محتویات سبد خرید",
                             on_delete=models.CASCADE)
    count = models.IntegerField("Count")
    product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "محتویات سبد خرید"
        verbose_name_plural = "محتویات سبد خرید"

    def __str__(self) -> str:
        return f"{self.product.name}"


class OrderItems(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', verbose_name="اقلام سفارش", on_delete=models.CASCADE)
    count = models.IntegerField("تعداد")
    product = models.ForeignKey(Product, verbose_name="محصول", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "اقلام سفارش"
        verbose_name_plural = 'اقلام فاکتور'

    def __str__(self) -> str:
        return f"{Product.name}"

    @property
    def item_cost(self):
        return self.count * self.product.price

    @property
    def item_discount(self):
        return self.product.total_discount * self.count
