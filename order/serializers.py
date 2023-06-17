from rest_framework import serializers
from .models import Order, OrderItems, Product
from customers.models import Customer, Address


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['get_full_name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'discount_price', 'total_discount']


class OrderItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItems
        fields = ['id', 'order', 'product', 'count']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    order_items = OrderItemsSerializer(many=True, read_only=True)
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'address', 'status', 'order_items']

