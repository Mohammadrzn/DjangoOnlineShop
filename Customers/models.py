from django.db import models
from Core.models import BaseModel
from .managers import CustomerManager
from django.contrib.auth.models import AbstractUser, Group


class Customer(AbstractUser, BaseModel):
    mobile = models.SmallIntegerField("موبایل", help_text="مثال: 9123456789", null=True, blank=True)
    telephone = models.SmallIntegerField("تلفن", help_text="شماره کامل همراه با کد شهر", null=True, blank=True)
    national_id = models.CharField("کد ملی", max_length=10, null=True, blank=True)
    age = models.SmallIntegerField("سن", null=True, blank=True)
    created_at = None

    ROLE_CHOICES = (
        ("A", "ادمین"),
        ("O", "ناظر"),
        ("C", "مشتری")
    )
    role = models.CharField("نقش", choices=ROLE_CHOICES, max_length=1, default="C", null=False, blank=False)

    GENDER_CHOICES = (
        ("F", "آقا"),
        ("M", "خانم")
    )
    gender = models.CharField("جنسیت", choices=GENDER_CHOICES, max_length=1, null=True, blank=True)

    objects = CustomerManager()

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Address(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    state = models.CharField("استان", max_length=75, null=False, blank=False)
    city = models.CharField("شهر", max_length=100, null=False, blank=False)
    full_address = models.TextField("آدرس", help_text="آدرس کامل همراه با شماره پلاک و واحد", null=False, blank=False)
    postal_code = models.SmallIntegerField("کد پستی", null=False, blank=False)
    is_deleted = None

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"

    def __str__(self):
        return f"{self.customer_id}"
