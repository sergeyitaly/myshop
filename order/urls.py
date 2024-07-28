from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Create a router instance
router = DefaultRouter()
# Register viewsets with the router
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'telegram_users', TelegramUserViewSet, basename='telegramuser')

urlpatterns = [
    # Include all routes registered with the router
    path('', include(router.urls)),
    path('order/', create_order, name='create-order'),
    path('order/<int:order_id>/', get_order, name='get_order'),
    path('telegram_webhook/', telegram_webhook, name='telegram_webhook'),
    path('health_check/', health_check, name='health_check'),

]

