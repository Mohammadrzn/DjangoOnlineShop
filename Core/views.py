from django.shortcuts import render
from rest_framework.views import APIView
from Product.models import Product, Category


class Home(APIView):
    @staticmethod
    def get(request):
        new_products = Product.objects.filter(count__gt=0, discount_percent=0)[0:6]
        discount_product = Product.objects.filter(count__gt=0, discount_percent__gt=0)

        return render(request, "home.html", {
            "new_products": new_products,
            "discount_product": discount_product
        })
