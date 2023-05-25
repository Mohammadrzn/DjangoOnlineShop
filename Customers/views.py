from django.shortcuts import render, redirect
from .forms import SignupForm
from .serializers import CustomerCreateSerializer
from djoser.views import UserViewSet
from rest_framework.permissions import AllowAny
from .models import Customer


class CustomerViewSet(UserViewSet):
    queryset = Customer.objects.all()
    permission_classes = [AllowAny]


def show_profile(request):
    return render(request, "profile.html")


def signup(request):
    errors = {}
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            serializer = CustomerCreateSerializer(data=form.cleaned_data)
            if serializer.is_valid():
                serializer.save()
                return redirect('login')
            else:
                errors = serializer.errors
        else:
            errors = form.errors
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form, 'errors': errors})


def login(request):
    return render(request, "login.html")


def contact(request):
    return render(request, "contact.html")
