from django.shortcuts import render


def show_profile(request):
    return render(request, "profile.html")


def login(request):
    return render(request, "login.html")


def contact(request):
    return render(request, "contact.html")
