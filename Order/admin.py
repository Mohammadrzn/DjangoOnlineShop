from django.contrib import admin
from .models import Order


@admin.register(Order)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["customer", "persian_created_at", "persian_edited_at", "persian_deleted_at"]
