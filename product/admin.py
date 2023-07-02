from .models import Product, Category, Comment, Discount
from django.contrib import admin

admin.site.register(Comment)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "persian_created_at", "persian_edited_at"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ["name", "category"]
    list_display = ["name", "price", "get_price", "count", "persian_created_at", "persian_edited_at", "image_tag"]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ["type", "amount", "discount_for", "persian_created_at", "persian_edited_at", "status"]
