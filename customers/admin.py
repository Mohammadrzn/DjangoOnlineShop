from django.contrib import admin
from .models import Customer, Address

admin.site.register(Address)


@admin.register(Customer)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["username", "mobile", "email"]
    list_display = ["username", "get_full_name", "mobile", "email", "date_joined", "persian_edited_at",
                    "persian_deleted_at"]
