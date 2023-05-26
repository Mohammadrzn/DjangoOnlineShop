from Core.models import BaseModel
from Customers.models import Customer
from django.db import models


class Category(BaseModel):
    name = models.CharField("نام", max_length=100, null=False, blank=False)
    inner_category = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return f"{self.name}"


class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="category_product")
    name = models.CharField("نام", max_length=100, null=False, blank=False)
    price = models.FloatField("قیمت", null=False, blank=False)
    count = models.SmallIntegerField("تعداد باقی مانده", null=False, blank=False)
    brand = models.CharField("برند", max_length=75, null=False, blank=False)
    description = models.TextField("توضیحات", null=False, blank=False)
    image = models.ImageField("تضویر", upload_to="Product_images", null=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "محصولات"

    def __str__(self):
        return f"{self.name}"


class Comment(BaseModel):
    title = models.CharField("موضوع", max_length=100, null=False, blank=False)
    content = models.TextField("متن نظر", null=False, blank=False)
    user = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "نظرات"

    def __str__(self):
        return f"{self.title}"
