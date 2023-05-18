from django.shortcuts import render
from Product.models import Product, Category


def home(request):
    products = Product.objects.filter(is_sold_out=False)[0:6]
    return render(request, "home.html", {"products": products})
