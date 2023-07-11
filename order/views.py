from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics
from rest_framework import status

from .serializers import OrderSerializer
from .models import Order, OrderItems
from customers.models import Address
from product.models import Product
from product.cart import Cart


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

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        customer = request.user
        if not customer:
            return Response({"detail": "login please"}, status=401)
        address = Address.objects.filter(customer=customer, is_default=True).first()
        insufficient_stock = False
        for item in cart:
            product_data = item['product']
            product = get_object_or_404(Product, pk=product_data['pk'])
            quantity = item['quantity']
            if quantity > product.count:
                insufficient_stock = True
                break
        if insufficient_stock:
            return Response({'error': 'موجودی کافی نیست'}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.create(customer=customer, address=address)
        for item in cart:
            product_data = item['product']
            product = get_object_or_404(Product, pk=product_data['pk'])
            quantity = item['quantity']
            if quantity <= product.count:
                OrderItems.objects.create(order=order, product=product, count=quantity)
                product.count -= quantity
                product.save()
        cart.clear()
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UpdateStatusView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


def order(request, id):
    order = get_object_or_404(Order, pk=id)
    return render(request, "order.html", {"order": order})
