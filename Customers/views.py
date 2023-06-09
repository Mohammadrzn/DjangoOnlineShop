from .serializers import CustomerSerializer, ProfileSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Customer
import datetime
import jwt


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
        return redirect("auth:profile")


class Login(APIView):
    @staticmethod
    def get(request):
        return render(request, "login.html")

    @staticmethod
    def post(request):
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


class Logout(APIView):
    @staticmethod
    def get(request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {
            "message": "success"
        }
        return redirect("http://127.0.0.1:8000")


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


def contact(request):
    return render(request, "contact.html")
