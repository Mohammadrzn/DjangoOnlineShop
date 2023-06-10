from django.urls import path
from . import views

app_name = "product"
urlpatterns = [
    path('<int:pk>/', views.detail, name="detail"),
    path('categories/', views.main_category, name="category"),
    path('categories/products/<int:pk>/', views.category_product, name="product_category"),
    path('order/', views.order_page, name="order_page"),
    path('cart/', views.CartShow.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', views.CartAddView.as_view(), name='add'),
    path('cart/mines/<int:product_id>/', views.CartMinesView.as_view(), name='mines'),
    path('cart/remove/<int:product_id>/', views.CartRemoveView.as_view(), name='remove'),
    path('clear/', views.ClearCartView.as_view(), name='clear'),
]
