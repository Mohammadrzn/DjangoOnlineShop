from django.contrib import admin
from django.urls import path, include
from Core.views import Home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', Home.as_view(), name="home"),
                  path('user/', include('Customers.urls')),
                  path('product/', include("Product.urls")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
