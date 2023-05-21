from django.db import models
import jdatetime


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=jdatetime.datetime.now, null=False, blank=False)
    edited_at = models.DateTimeField(default=jdatetime.datetime.now, null=False, blank=False)
    deleted_at = models.DateTimeField(default=jdatetime.datetime.now, null=False, blank=False)
    is_deleted = models.BooleanField("Is Deleted", default=False, null=False, blank=False)

    class Meta:
        abstract = True
