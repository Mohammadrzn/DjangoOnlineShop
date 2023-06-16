from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CartSerializer
from .models import Product, Category
from .cart import Cart


def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category, count__gt=0).exclude(pk=pk)[0:9]
    return render(request, "detail.html", {
        "product": product,
        "related_products": related_products
    })


def order_page(request):
    return render(request, "cart.html")


def main_category(request):
    categories = Category.objects.filter(upper_category=None)
    return render(request, 'home.html', {
        'categories': categories,
    })


def category_product(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category_products = Product.objects.filter(category=category, count__gt=0)
    return render(request, "category.html", {
        "category": category,
        "category_products": category_products,
    })


class CartShow(APIView):
    @staticmethod
    def get(request):
        return render(request, "cart.html")


class CartAddView(APIView):
    @staticmethod
    def post(request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product, quantity=1)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartMinesView(APIView):
    @staticmethod
    def get(request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product, quantity=-1)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartRemoveView(APIView):
    @staticmethod
    def get(request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class ClearCartView(APIView):
    @staticmethod
    def get(request):
        cart = Cart(request)
        cart.clear()
        serializer = CartSerializer(cart)
        return Response(serializer.data)
