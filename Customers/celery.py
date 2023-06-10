from django.conf import settings
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoOnlineShop.settings')
app = Celery('DjangoOnlineShop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
