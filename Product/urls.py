from django.urls import path
from . import views

app_name = "product"
urlpatterns = [
    path('<int:pk>/', views.detail, name="detail"),
    path('categories/', views.main_category, name="category"),
    path('categories/products/<int:pk>/', views.category_product, name="product_category"),
    path('order/',views.order_page, name="order_page"),
]
