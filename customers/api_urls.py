from django.urls import path
from . import api_views

app_name = "api"

urlpatterns = [
    path('login/', api_views.Login.as_view(), name='login'),
    path('signup/', api_views.Signup.as_view(), name='signup'),
    path('change/', api_views.Change.as_view(), name='change'),
    path('logout/', api_views.logout, name="logout"),
    path('login/otp/', api_views.Otp.as_view(), name='otp'),
    path('profile/', api_views.profile, name="profile"),
    path('verification/', api_views.Verification.as_view(), name='verification'),
    path('address/change/', api_views.ChangeAddress.as_view(), name='change_address'),
    path('contact_us/', api_views.contact_us, name='contact_us'),
    path('information/', api_views.information, name="information"),
    path('addresses/', api_views.address, name="addresses"),
    # path('address/change/', api_views.ChangeAddress)
]
