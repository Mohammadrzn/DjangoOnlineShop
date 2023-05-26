from django.contrib import admin
from .models import Product, Category, Comment

admin.site.register(Product)
admin.site.register(Comment)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "persian_created_at", "persian_edited_at"]
