from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from .serializers import CustomerCreateSerializer
from djoser.views import UserViewSet
from rest_framework.permissions import AllowAny
from .models import Customer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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


def my_login(request):
    errors = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = get_user_model().objects.get(username=username)

            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)
                request.session['jwt_token'] = token

                return redirect('home')
            else:
                errors['authentication'] = 'Invalid username or password'
        else:
            errors = form.errors
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'errors': errors})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_auth(request):
    return Response({'message': 'Authenticated'}, status=200)


def contact(request):
    return render(request, "contact.html")
