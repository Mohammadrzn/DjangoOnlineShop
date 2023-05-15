from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now, null=False, blank=False)
    is_deleted = models.BooleanField("Is Deleted", default=False, null=False, blank=False)

    class Meta:
        abstract = True


class User(AbstractUser):
    mobile = models.SmallIntegerField(max_length=10,
                                      help_text="Example: 9123456789",
                                      unique=True, null=False, blank=False)
    telephone = models.SmallIntegerField(help_text="Enter without your city code", max_length=11, null=True, blank=True)
    national_id = models.CharField(max_length=10, null=True, blank=True)
    age = models.SmallIntegerField(max_length=3, null=True, blank=True)

    GENDER_CHOICES = (
        ("F", "Femail"),
        ("M", "Mail")
    )
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, null=True, blank=True)
