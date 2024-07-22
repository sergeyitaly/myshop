# order/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, create_order, telegram_webhook

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('order/', create_order, name='create-order'),
    path('telegram-webhook/', telegram_webhook, name='telegram-webhook'),

]
