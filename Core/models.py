import datetime
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)
    edited_at = models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)
    deleted_at = models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)
    is_deleted = models.BooleanField("Is Deleted", default=False, null=False, blank=False)

    class Meta:
        abstract = True
