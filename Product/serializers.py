from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'total_discount', 'discount_price']


class CartSerializer(serializers.Serializer):
    total_price = serializers.SerializerMethodField()
    total_discount = serializers.SerializerMethodField()
    total_price_discount = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    @staticmethod
    def get_total_price(obj):
        return obj.get_total_price()

    @staticmethod
    def get_total_discount(obj):
        return obj.get_total_discount()

    @staticmethod
    def get_total_price_discount(obj):
        return obj.get_total_price_discount()

    @staticmethod
    def get_items(obj):
        return list(obj)

    @staticmethod
    def update_totals(obj):
        total_price = 0
        total_discount = 0
        for item in obj:
            total_price += item['total_price']
            total_discount += item['discount']
        obj.total_price = total_price
        obj.total_discount = total_discount
        obj.total_price_discount = total_price - total_discount

    def to_representation(self, instance):
        self.update_totals(instance)
        return super().to_representation(instance)
