from Core.models import BaseModel
from Customers.models import Customer
from django.db import models
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError


class Discount(BaseModel):
    type_choice = (('c', 'نقدی'), ('p', 'درصدی'))
    discount_for_choice = (("p", "محصول"), ("c", "دسته بندی"), ("u", "مشتری"))
    type = models.CharField("نوع تخفیف", choices=type_choice, max_length=1, null=True, blank=True)
    amount = models.IntegerField("مقدار تخفیف")
    status = models.BooleanField("تمام شده", default=False)
    discount_for = models.CharField("تخفیف برای", choices=discount_for_choice, max_length=1, null=True, blank=True)

    class Meta:
        verbose_name = "تخفیف"
        verbose_name_plural = "تخفیف ها"

    def __str__(self):
        return str(self.amount)

    def clean(self):
        if self.type == 'p':
            if self.amount < 0 or self.amount > 100:
                raise ValidationError("مقدار تخفیف باید بین 0 تا 100 درصد باشد")
        elif self.type == 'c':
            if self.amount < 0:
                raise ValidationError("مقدار تخفیف نمی تواند از قیمت محصول بیشتر باشد")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Category(BaseModel):
    name = models.CharField("نام", max_length=100, null=False, blank=False)
    upper_category = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE,
                                       verbose_name="دسته بندی اصلی")
    discount = models.ForeignKey(Discount, related_name='category_discount', verbose_name="تخفیف دسته بندی",
                                 on_delete=models.CASCADE, null=True, blank=True)

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
    discount = models.ForeignKey(Discount, related_name='product_discount', verbose_name="تخفیف محصول",
                                 on_delete=models.CASCADE, null=True, blank=True)

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % self.image)

    image_tag.allow_tags = True

    image_tag.short_description = 'تصویر محصول'

    def total_discount(self):
        product_discount = 0
        if self.discount:
            if self.discount.type == 'c':
                product_discount += self.discount.amount
            elif self.discount.type == 'p':
                product_discount += (self.price * self.discount.amount) / 100

        category_discount = 0
        if self.category.discount:
            if self.category.discount.type == 'c':
                category_discount += self.category.discount.amount
            elif self.category.discount.type == 'p':
                category_discount += (self.price * self.category.discount.amount) / 100

        total_discount = product_discount + category_discount
        return int(total_discount)

    def get_price(self):
        return self.price - self.total_discount()

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
