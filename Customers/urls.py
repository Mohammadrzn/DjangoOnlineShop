from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.show_profile, name='profile'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('login/', views.Login.as_view(), name='login'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('user/', views.CustomerView.as_view(), name='user'),
    path('contact_us/', views.contact, name='contact_us'),
]
