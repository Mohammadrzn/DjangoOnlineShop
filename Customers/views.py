from .serializers import CustomerSerializer, ProfileSerializer, AddressSerializer, SendOtpSerializer, VerificationSerializer
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from rest_framework.exceptions import AuthenticationFailed
from .tasks import send_otp_email, send_otp_sms
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Customer
import datetime
import redis
import jwt
import re


class ShowProfile(APIView):
    @staticmethod
    def get(request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("برای دسترسی به این صفحه ابتدا وارد اکانت خود شوید")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
            user = Customer.objects.filter(id=payload["id"]).first()
            if not user:
                raise AuthenticationFailed("کاربری با این مشخصات یافت نشد")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("برای دسترسی به این صفحه ابتدا وارد اکانت خود شوید")

        return render(request, "profile.html")


class Signup(APIView):
    @staticmethod
    def get(request):
        return render(request, "signup.html", context={})

    @staticmethod
    def post(request):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return authenticate(request)


class Login(APIView):
    @staticmethod
    def get(request):
        return render(request, "login.html")

    @staticmethod
    def post(request):
        return authenticate(request)


class Logout(APIView):
    @staticmethod
    def get(request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {
            "message": "success"
        }
        return response


class Information(APIView):
    @staticmethod
    def get(request):

        token = request.COOKIES.get("jwt")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
            user = Customer.objects.filter(id=payload["id"]).first()
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("برای دسترسی به این صفحه ابتدا وارد اکانت خود شوید")

        return render(request, "information.html", {
            "user": user,
        })


class Change(APIView):
    @staticmethod
    def get(request):
        serializer = ProfileSerializer
        return render(request, "change.html", {"serializer": serializer})

    @staticmethod
    def post(request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("برای دسترسی به این صفحه ابتدا وارد اکانت خود شوید")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
            user = Customer.objects.filter(id=payload["id"]).first()
            if not user:
                raise AuthenticationFailed("کاربری با این مشخصات یافت نشد")

            elif request.method == "POST":
                serializer = ProfileSerializer(user, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return redirect("auth:change")
                else:
                    return render(request, "change.html", {"serializer": serializer})
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("برای دسترسی به این صفحه ابتدا وارد اکانت خود شوید")


class Address(APIView):
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

    token = jwt.encode(payload, "secret", algorithm="HS256")

    response = HttpResponseRedirect(reverse("auth:profile"))
    response.set_cookie(key="jwt", value=token, httponly=True)
    response.data = {
        "message": "success"
    }

    return response
