from Core.models import BaseModel
from Customers.models import Customer
from django.db import models
from django.utils.html import mark_safe


class Category(BaseModel):
    name = models.CharField("نام", max_length=100, null=False, blank=False)
    upper_category = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE,
                                       verbose_name="دسته بندی اصلی")

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
    image = models.ImageField("تصویر", upload_to="Product_images", null=True, blank=True)
    discount_percent = models.SmallIntegerField("درصد تخفیف", null=False, blank=False,
                                                help_text="بدون علمات درصد وارد شود، اگر نخفیف ندارد 0 وارد کنید")

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % self.image)

    image_tag.allow_tags = True

    image_tag.short_description = 'تصویر محصول'

    def get_price(self):
        if self.discount_percent == 0:
            return self.price
        else:
            return self.price - (self.discount_percent / 100 * self.price)

    get_price.short_description = "قیمت پس از تخفیف"

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
