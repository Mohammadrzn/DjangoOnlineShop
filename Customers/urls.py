from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.show_profile, name='profile'),
    path('login/', views.Login.as_view(), name='login'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('contact_us/', views.contact, name='contact_us'),
]
