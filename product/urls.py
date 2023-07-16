from django.urls import path

from . import views

app_name = "product"

urlpatterns = [
    path('<int:pk>/', views.Detail.as_view(), name="detail"),
    path('categories/', views.MainCategory.as_view(), name="category"),
    path('categories/products/<int:pk>/', views.CategoryProduct.as_view(), name="product_category"),
    path('order/', views.OrderPage.as_view(), name="order_page"),
    path('', views.CartView.as_view(), name='cart'),
    path('cart/<int:product_id>/', views.CartView.as_view(), name='cart-product'),
    path('cart/', views.cart_view, name='cart_page'),
]
