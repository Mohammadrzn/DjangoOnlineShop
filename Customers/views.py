from django.shortcuts import render, redirect
from .forms import SignupForm


def show_profile(request):
    return render(request, "profile.html")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = SignupForm

    return render(request, "signup.html", {
        "form": form
    })


def login(request):
    return render(request, "login.html")


def contact(request):
    return render(request, "contact.html")
