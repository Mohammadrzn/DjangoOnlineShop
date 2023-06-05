from django.urls import path
from . import views

app_name = "auth"
urlpatterns = [
    path('profile/', views.show_profile, name='profile'),
    path('change/', views.Change.as_view(), name='change'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('login/', views.Login.as_view(), name='login'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('contact_us/', views.contact, name='contact_us'),
]
