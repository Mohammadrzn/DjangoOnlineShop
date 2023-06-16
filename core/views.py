from django.shortcuts import render
from rest_framework.views import APIView
from product.models import Product, Category, Discount


class Home(APIView):
    @staticmethod
    def get(request):
        new_products = Product.objects.filter(count__gt=0, )[0:6]
        discount_product = Product.objects.filter(count__gt=0, discount=True)
        discount = Discount.objects.get(discount_for="p")

        return render(request, "home.html", {
            "new_products": new_products,
            "discount_product": discount_product,
            "discount": discount,
        })
