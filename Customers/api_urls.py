from django.urls import path
from . import api_views


app_name = "api"

urlpatterns = [
    path('profile/', api_views.ShowProfile.as_view(), name='profile'),
    path('change/', api_views.Change.as_view(), name='change'),
    path('information/', api_views.Information.as_view(), name='information'),
    path('logout/', api_views.Logout.as_view(), name='logout'),
    path('login/otp/', api_views.Otp.as_view(), name='otp'),
    path('verification/', api_views.Verification.as_view(), name='verification'),
    path('addresses/', api_views.Address.as_view(), name='addresses'),
    path('address/change/', api_views.ChangeAddress.as_view(), name='change_address'),
]