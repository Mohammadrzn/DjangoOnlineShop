from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from django.views import View

from .serializers import CartSerializer
from .models import Product, Category
from .cart import Cart


class Detail(View):
    @staticmethod
    def get(request, pk):
        product = get_object_or_404(Product, pk=pk)
        related_products = Product.objects.filter(category=product.category, count__gt=0).exclude(pk=pk)[0:9]
        return render(request, "detail.html", {
            "product": product,
            "related_products": related_products
        })


class OrderPage(View):
    @staticmethod
    def get(request):
        return render(request, "cart.html")


class MainCategory(View):
    @staticmethod
    def get(request):
        categories = Category.objects.filter(upper_category=None)
        return render(request, 'home.html', {
            'categories': categories,
        })


class CategoryProduct(View):
    @staticmethod
    def get(request, pk):
        category = get_object_or_404(Category, pk=pk)
        category_products = Product.objects.filter(category=category, count__gt=0)
        return render(request, "category.html", {
            "category": category,
            "category_products": category_products,
        })


class CartView(View):
    @staticmethod
    def get(request):
        cart = Cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


def cart_view(request):
    return render(request, "cart.html")
