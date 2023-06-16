from django.urls import path
from . import api_views

app_name = "api"

urlpatterns = [
    path('login/', api_views.Login.as_view(), name='login'),
    path('signup/', api_views.Signup.as_view(), name='signup'),
    path('change/', api_views.Change.as_view(), name='change'),
    path('login/otp/', api_views.Otp.as_view(), name='otp'),
    path('verification/', api_views.Verification.as_view(), name='verification'),
    path('address/change/', api_views.ChangeAddress.as_view(), name='change_address'),
]
