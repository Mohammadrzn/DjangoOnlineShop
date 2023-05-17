from Core.models import BaseModel
from Customers.models import Customer
from django.db import models


class Category(BaseModel):
    name = models.CharField("Name", max_length=100, null=False, blank=False)

    class Meta:
        ordering = "name"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"


class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    name = models.CharField("Name", max_length=100, null=False, blank=False)
    price = models.IntegerField("Price", null=False, blank=False)
    count = models.SmallIntegerField(null=False, blank=False)
    brand = models.CharField("Brand", max_length=75, null=False, blank=False)
    description = models.TextField(null=False, blank=False)

    class Meta:
        ordering = "name"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.name}"


class Comment(BaseModel):
    title = models.CharField("Title", max_length=100, null=False, blank=False)
    content = models.TextField("Content", null=False, blank=False)
    user = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"{self.title}"
