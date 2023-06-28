from django.contrib import admin
from django.urls import path, include
from core.views import Home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name="home"),
    path('user/', include('customers.api_urls')),
    path('product/', include("product.urls")),
    path('orders/', include('order.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
