# order/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, create_order, telegram_webhook

# Create a router instance
router = DefaultRouter()
# Register viewsets with the router
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    # Include all routes registered with the router
    path('', include(router.urls)),
    path('order/', create_order, name='create-order'),
    path('telegram-webhook/', telegram_webhook, name='telegram-webhook'),
]
