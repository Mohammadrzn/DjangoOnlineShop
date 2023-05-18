from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.show_profile, name='profile'),
    path('login/', views.login, name='login'),
    path('contact_us/', views.contact, name='contact_us'),
]
