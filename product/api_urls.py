from django.urls import path

from . import api_views

app_name = "api_product"

urlpatterns = [
    path('clear/', api_views.ClearCartView.as_view(), name='clear'),
    path('cart/<int:product_id>/', api_views.CartView.as_view(), name='cart-product'),
]
