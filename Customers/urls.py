from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.show_profile, name='profile'),
    path('login/', views.my_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('check-auth/', views.check_auth, name='check_auth'),
    path('contact_us/', views.contact, name='contact_us'),
]
