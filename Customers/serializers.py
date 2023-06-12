from rest_framework import serializers
from .models import Customer, Address


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'mobile', 'telephone', 'national_id', 'age', 'gender']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


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
