from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import OrderSerializer
from customers.models import Address
from rest_framework import generics
from product.models import Product
from product.cart import Cart
from .models import Order, OrderItems


class OrderCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        customer = self.get_object()
        address = get_object_or_404(Address, customer=customer)
        serializer = self.get_serializer(address)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        cart = Cart(request)
        customer = self.get_object()
        address = get_object_or_404(Address, customer=customer)

        # Check stock availability for all products in the cart
        insufficient_stock = False
        for item in cart:
            product_data = item['product']
            product = get_object_or_404(Product, pk=product_data['pk'])
            quantity = item['quantity']
            if quantity > product.count:
                insufficient_stock = True
                break

        if insufficient_stock:
            return Response({'error': 'موجودی کافی نیست'})

        # Create the order instance
        order = Order.objects.create(customer=customer, address=address)

        for item in cart:
            product_data = item['product']
            product = get_object_or_404(Product, pk=product_data['pk'])
            quantity = item['quantity']

            if quantity <= product.count:
                OrderItems.objects.create(order=order, product=product, count=quantity)
                product.stock -= quantity
                product.save()

        cart.clear()
        serializer = self.get_serializer(order)
        return Response(serializer.data)
