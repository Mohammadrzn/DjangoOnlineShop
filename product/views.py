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


class CartView(APIView):
    def get(self, request):
        cart = Cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        quantity = request.data.get('quantity', 1)
        cart.add(product, quantity=quantity)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def patch(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        action = request.data.get('action')

        if action == 'increment':
            cart.add(product, quantity=1)
        elif action == 'decrement':
            quantity = cart.cart.get(str(product.id), {}).get('quantity', 0)
            if quantity > 1:
                cart.add(product, quantity=-1)
            else:
                cart.remove(product)

        total_price = cart.get_total_price()
        total_discount = cart.get_total_discount()
        total_price_discount = total_price - total_discount

        serializer = CartSerializer(cart)
        return Response({
            'cart': serializer.data,
            'total_price': total_price,
            'total_discount': total_discount,
            'total_price_discount': total_price_discount,
        })

    def delete(self, request, product_id=None):
        cart = Cart(request)

        if product_id is not None:
            product = get_object_or_404(Product, id=product_id)
            cart.remove(product)
        else:
            cart.clear()

        serializer = CartSerializer(cart)
        return Response(serializer.data)


def cart_view(request):
    return render(request, "cart.html")


class ClearCartView(APIView):
    def delete(self, request):
        cart = Cart(request)
        cart.clear()
        serializer = CartSerializer(cart)
        return Response(serializer.data)
