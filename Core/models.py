from django.db import models
from jalali_date import datetime2jalali


class BaseModel(models.Model):
    created_at = models.DateTimeField("ایجاد شده در", null=True, blank=True)
    edited_at = models.DateTimeField("ویراش شده در", null=True, blank=True)
    deleted_at = models.DateTimeField("پاک شده در", null=True, blank=True)
    is_deleted = models.BooleanField("حذف شده", default=False, null=False, blank=False)

    def jdatetime(self):
        return datetime2jalali(self.created_at).strftime('%Y/%m/%d %H:%M:%S')

    jdatetime.short_description = "تاریخ"

    class Meta:
        abstract = True
