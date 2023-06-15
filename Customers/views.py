from .serializers import LoginSerializer, ProfileSerializer, AddressSerializer, SendOtpSerializer, VerificationSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .tasks import send_otp_email, send_otp_sms
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
from django.views import View
from .models import Customer
from jwt import encode
from .mixin import *
import datetime
import redis
import re


class ShowProfile(APIView):
    @staticmethod
    def get(request):
        token = request.COOKIES.get("jwt")

        if token:
            return render(request, "profile.html")
        else:
            return redirect("auth:login")


class Signup(APIView):
    @staticmethod
    def get(request):
        return render(request, "signup.html", context={})

    @staticmethod
    def post(request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return authenticate(request)


class Login(APIView):
    serializer_class = LoginSerializer

    @staticmethod
    def get(request):
        return render(request, "login.html")

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            response = HttpResponse(status=status.HTTP_200_OK)
            response.set_cookie('jwt', access_token, httponly=True)
            return response
        else:
            error_message = 'نام کاربری یا رمز عبور اشتباه است'
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    @staticmethod
    def get(request):
        url = reverse('home')
        response = HttpResponseRedirect(url)
        response.delete_cookie("jwt")
        return response


class Information(View):
    @staticmethod
    def get(request):
        return render(request, "information.html")


class Change(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.serializer = ProfileSerializer()

    def get(self, request):
        return render(request, "change.html", {"serializer": self.serializer})

    def post(self, request):
        token = request.COOKIES.get("jwt")
        self.serializer = ProfileSerializer(data=request.data)

        if token:
            if self.serializer.is_valid():
                self.serializer.save()
                return redirect("auth:information")
            else:
                return render(request, "change.html", {"serializer": self.serializer})
        else:
            return redirect("auth:login")


class Address(View):
    @staticmethod
    def get(request):
        return render(request, "addresses.html")


class ChangeAddress(APIView):
    @staticmethod
    def get(request):
        return render(request, "change_address.html")

    @staticmethod
    def post(request):
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response()


def contact(request):
    return render(request, "contact.html")


class Otp(APIView):
    @staticmethod
    def get(request):
        serializer = SendOtpSerializer
        return render(request, 'login_otp.html', {'serializer': serializer})

    @staticmethod
    def post(request):
        print("Are we in post method")
        serializer = SendOtpSerializer(data=request.data)
        print("Is serializer valid")
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid():
            user = None
            mail_phone = serializer.validated_data.get('mail_phone')
            print(mail_phone)
            if re.match(r'^[A-Za-z0-9]+[-._]*[A-Za-z0-9]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}$', mail_phone):
                try:
                    user = Customer.objects.get(email=mail_phone)
                except Customer.DoesNotExist:
                    pass
                if user:
                    send_otp_email.delay(mail_phone)
                    response = redirect('auth:verification')
                    response.set_cookie('user_email_or_phone', mail_phone)
                    return response
            elif re.match(r'09(\d{9})$', mail_phone):
                print("BEFORE TRY")
                print(Customer.objects.values('mobile'))
                print(type(mail_phone))
                try:
                    user = Customer.objects.get(mobile=mail_phone)
                except Customer.DoesNotExist:
                    pass
                if user:
                    send_otp_sms.delay(mail_phone, 60)
                    response = redirect('auth:verification')
                    response.set_cookie('user_email_or_phone', mail_phone)
                    return response

        return render(request, 'verification.html', {'serializer': serializer})


class Verification(APIView):
    @staticmethod
    def get(request):
        serializer = VerificationSerializer()
        return render(request, "verification.html", {"serializer": serializer})

    @staticmethod
    def post(request):
        serializer = VerificationSerializer(request.POST)
        if serializer.is_valid:
            verification_code = serializer['verification_code']
            user_identifier = request.COOKIES.get('user_email_or_phone')
            r = redis.Redis(host='localhost', port=6379, db=0)
            stored_code = r.get(user_identifier).decode()
            if verification_code == stored_code:
                user = Customer.objects.filter(Q(email=user_identifier) | Q(phone_number=user_identifier)).first()
                if user:
                    pass

        return render(request, "verification.html", {"serializer": serializer})


def authenticate(request):
    username = request.data["username"]
    password = request.data["password"]

    user = Customer.objects.filter(username=username).first()

    if user is None:
        raise AuthenticationFailed("کاربری با این مشخصات یافت نشد")

    if not user.check_password(password):
        raise AuthenticationFailed("رمز اشتباه است")

    payload = {
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=10),
        "iat": datetime.datetime.utcnow()
    }

    token = encode(payload, "secret", algorithm="HS256")

    response = HttpResponseRedirect(reverse("auth:profile"))
    response.set_cookie(key="jwt", value=token, httponly=True)
    response.data = {
        "message": "success"
    }

    return response
