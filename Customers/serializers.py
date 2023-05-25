from djoser.serializers import UserCreateSerializer, UserSerializer
from .models import Customer


class CustomerCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = Customer
        fields = ("username", "password")


class CustomerSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Customer
