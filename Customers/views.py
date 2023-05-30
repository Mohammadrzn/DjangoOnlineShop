from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from .serializers import CustomerSerializer
from rest_framework.views import APIView
from django.shortcuts import render
from .models import Customer
import jwt, datetime


def show_profile(request):
    return render(request, "profile.html")


class Signup(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Login(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        user = Customer.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed("کاربری با این مشخصات یافت نشد")

        if not user.check_password(password):
            raise AuthenticationFailed("رمز اشتباه است")

        payload = {
            "id": user.id,
            "exp": datetime.datetime.now() + datetime.timedelta(days=10),
            "iat": datetime.datetime.now()
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")

        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            "message": "success"
        }

        return response


class CustomerView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("برای دسترسی به این صفحه ابتدا وارد اکانت خود شوید")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("برای دسترسی به این صفحه ابتدا وارد اکانت خود شوید")

        user = Customer.objects.filter(id=payload["id"]).first()
        serializer = CustomerSerializer(user)

        return Response(serializer.data)


def contact(request):
    return render(request, "contact.html")
