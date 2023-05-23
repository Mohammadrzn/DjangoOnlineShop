from django.contrib import admin
from .models import Customer, Address

admin.site.register(Address)


@admin.register(Customer)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["get_full_name", "persian_created_at", "persian_edited_at", "persian_deleted_at"]
