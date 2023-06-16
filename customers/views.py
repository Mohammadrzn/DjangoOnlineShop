from django.shortcuts import render, redirect
from .mixin import *


def signup(request):
    return render(request, "signup.html")


def login(request):
    return render(request, "login.html")


def contact(request):
    return render(request, "contact.html")


def show_profile(request):
    token = request.COOKIES.get("jwt")
    if token:
        return render(request, "profile.html")
    else:
        return redirect("auth:login")


def information(request):
    return render(request, "information.html")


def address(request):
    return render(request, "addresses.html")


def logout(request):
    url = reverse('home')
    response = HttpResponseRedirect(url)
    response.delete_cookie("jwt")
    return response
