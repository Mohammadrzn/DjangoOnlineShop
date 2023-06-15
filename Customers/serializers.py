from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Customer, Address
from jwt import decode


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    tokens = serializers.SerializerMethodField()

    @staticmethod
    def get_tokens(obj):
        user = Customer.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        user = authenticate(username=username, password=password)

        if user is None:
            raise AuthenticationFailed('Invalid credentials, try again')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        attrs['user'] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'mobile', 'telephone', 'national_id', 'age', 'gender']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'state', 'city', 'full_address', 'postal_code', 'customer']

    def create(self, validated_data):
        request = self.context['request']
        token = request.COOKIES.get("jwt")
        payload = decode(token, "secret", algorithms=["HS256"])
        customer_id = payload["id"]

        validated_data['customer_id'] = customer_id
        address = super().create(validated_data)

        return address


class SendOtpSerializer(serializers.Serializer):
    mail_phone = serializers.CharField(error_messages={
        'required': 'وارد کردن این فیلد الزامی',
        'invalid': 'شماره همراه یا ایمیل معتبر نمی باشد.'
    })


class VerificationSerializer(serializers.Serializer):
    verification_code = serializers.CharField(max_length=6, error_messages={
        'required': 'وارد کردن این فیلد الزامی',
        'max_length': 'کد وارد شده بیش از حد مجاز می باشد.'
    })
