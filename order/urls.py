from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('details/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('update_status/<int:pk>/', views.UpdateStatusView.as_view(), name='update_status'),
]
