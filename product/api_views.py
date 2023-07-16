from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CartSerializer
from .models import Product
from .cart import Cart


class ClearCartView(APIView):
    @staticmethod
    def delete(request):
        cart = Cart(request)
        cart.clear()
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartView(APIView):
    @staticmethod
    def post(request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        quantity = request.data.get('quantity', 1)
        cart.add(product, quantity=quantity)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @staticmethod
    def patch(request, product_id):
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

    @staticmethod
    def delete(request, product_id=None):
        cart = Cart(request)

        if product_id is not None:
            product = get_object_or_404(Product, id=product_id)
            cart.remove(product)
        else:
            cart.clear()

        serializer = CartSerializer(cart)
        return Response(serializer.data)
