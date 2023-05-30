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

        token = jwt.encode(payload, "secret", algorithm="HS256").decode("utf-8")

        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            "message": "success"
        }

        return response


def contact(request):
    return render(request, "contact.html")
