from django.db import models
from jalali_date import datetime2jalali


class BaseModel(models.Model):
    created_at = models.DateTimeField("ایجاد شده در",auto_now_add=True, null=True, blank=True)
    edited_at = models.DateTimeField("ویراش شده در", null=True, blank=True)
    deleted_at = models.DateTimeField("پاک شده در", null=True, blank=True)
    is_deleted = models.BooleanField("حذف شده", default=False, null=False, blank=False)

    def persian_created_at(self):
        if self.created_at:
            return datetime2jalali(self.created_at).strftime('%Y/%m/%d %H:%M:%S')
        return None

    def persian_edited_at(self):
        if self.edited_at:
            return datetime2jalali(self.edited_at).strftime('%Y/%m/%d %H:%M:%S')
        else:
            return None

    def persian_deleted_at(self):
        if self.deleted_at:
            return datetime2jalali(self.deleted_at).strftime('%Y/%m/%d %H:%M:%S')
        return None

    persian_created_at.short_description = "تاریخ ایجاد"

    persian_edited_at.short_description = "تاریخ ویرایش"

    persian_deleted_at.short_description = "تاریخ حذف"

    class Meta:
        abstract = True
