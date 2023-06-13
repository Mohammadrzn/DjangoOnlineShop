from django.urls import path
from . import views

app_name = "auth"
urlpatterns = [
    path('profile/', views.ShowProfile.as_view(), name='profile'),
    path('change/', views.Change.as_view(), name='change'),
    path('information/', views.Information.as_view(), name='information'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('login/', views.Login.as_view(), name='login'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/otp/', views.Otp.as_view(), name='otp'),
    path('verification/', views.Verification.as_view(), name='verification'),
    path('addresses/', views.Address.as_view(), name='addresses'),
    path('address/change/', views.ChangeAddress.as_view(), name='change_address'),
    path('contact_us/', views.contact, name='contact_us'),
]
