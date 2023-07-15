from django.urls import path

from . import views

app_name = "auth"

urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('change/', views.Change.as_view(), name='change'),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('login/otp/', views.Otp.as_view(), name='otp'),
    path('profile/', views.Profile.as_view, name="profile"),
    path('verification/', views.Verification.as_view(), name='verification'),
    path('address/change/', views.ChangeAddress.as_view(), name='change_address'),
    path('contact_us/', views.ContactUs.as_view(), name='contact_us'),
    path('information/', views.Information.as_view(), name="information"),
    path('addresses/', views.AddressShow.as_view(), name="addresses"),
]
