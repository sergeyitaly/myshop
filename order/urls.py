from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet, TelegramUserViewSet, OrderSummaryViewSet, 
    create_order, get_order, get_orders, #get_order_summary, 
    get_order_summary_by_chat_id,
    update_order, telegram_webhook, health_check
)

# Create a router instance
router = DefaultRouter()
# Register viewsets with the router
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'telegram_users', TelegramUserViewSet, basename='telegramuser')
router.register(r'order_summary', OrderSummaryViewSet, basename='order_summary')

urlpatterns = [
    # Include all routes registered with the router
    path('', include(router.urls)),
    path('order/', create_order, name='create_order'),
    path('order/<int:order_id>/', get_order, name='get_order'),
    path('orders/', get_orders, name='get_orders'),
    path('order_summary/<int:chat_id>/', get_order_summary_by_chat_id, name='get_order_summary_by_chat_id'),

   # path('order_summary/', get_order_summary, name='get_order_summary'),
 #   path('update_order_summary/', update_order, name='update_order_summary'),  # Add this line for update_order_summary
    path('telegram_webhook/', telegram_webhook, name='telegram_webhook'),
    path('health_check/', health_check, name='health_check'),
]
