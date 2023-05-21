from django.shortcuts import render
from .forms import SignupForm


def show_profile(request):
    return render(request, "profile.html")


def signup(request):
    form = SignupForm

    return render(request, "signup.html", {
        "form": form
    })


def login(request):
    return render(request, "login.html")


def contact(request):
    return render(request, "contact.html")
