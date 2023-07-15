from django.shortcuts import render
from django.views import View

from . models import Address
from .mixin import *


class Signup(View):
    @staticmethod
    def get(request):
        return render(request, "signup.html")


class Login(View):
    @staticmethod
    def get(request):
        return render(request, "login.html")


class Change(View):
    @staticmethod
    def get(request):
        return render(request, "change.html")


class ChangeAddress(View):
    @staticmethod
    def get(request):
        return render(request, "change_address.html")


class Otp(View):
    @staticmethod
    def get(request):
        return render(request, 'login_otp.html')


class Verification(View):
    @staticmethod
    def get(request):
        return render(request, "verification.html")


class ContactUs(View):
    @staticmethod
    def get(request):
        return render(request, "contact.html")


class Profile(View):
    @staticmethod
    def get(request):
        return render(request, "profile.html")


class Information(View):
    @staticmethod
    def get(request):
        return render(request, "information.html")


class AddressShow(View):
    @staticmethod
    def get(request):
        address = Address.objects.values()
        return render(request, "addresses.html", {"address": address})


class Logout(View):
    @staticmethod
    def get(request):
        url = reverse('home')
        response = HttpResponseRedirect(url)
        response.delete_cookie("jwt")
        return response
