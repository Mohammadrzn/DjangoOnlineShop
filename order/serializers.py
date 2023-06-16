from rest_framework import serializers
from .models import Order
from customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['get_full_name']


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'address', 'status', 'order_items']


