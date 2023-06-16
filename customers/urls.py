from django.urls import path
from . import views

app_name = "auth"
urlpatterns = [
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('contact_us/', views.contact, name='contact_us'),
    path('profile/', views.show_profile, name='profile'),
    path('information/', views.information, name='information'),
    path('addresses/', views.address, name='addresses'),
]

