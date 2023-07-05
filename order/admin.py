from django.contrib import admin
from .models import Order, OrderItems, Carts


admin.site.register([Carts])


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer", "persian_created_at", "persian_edited_at", "persian_deleted_at"]


@admin.register(OrderItems)
class OrderItems(admin.ModelAdmin):
    list_display = ['id', 'product', 'item_cost']
    list_filter = ['product']
    search_fields = ['product']
    ordering = ['id']

    @staticmethod
    def product(obj):
        return obj.product.name
