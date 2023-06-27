from django.shortcuts import render
from django.views import View
from product.models import Product, Category, Discount


class Home(View):
    @staticmethod
    def get(request):
        new_products = Product.objects.filter(count__gt=0, discount_id=None)[0:6]
        discount_product = Product.objects.filter(count__gt=0, discount__isnull=False)
        discount = Discount.objects.get(discount_for="p")
        category = Category.objects.values()

        return render(request, "home.html", {
            "new_products": new_products,
            "discount_product": discount_product,
            "discount": discount,
            "category": category,
        })
