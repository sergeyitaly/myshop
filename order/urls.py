from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet, create_order, send_email  # Import the view functions and viewsets

app_name = "orders"

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create-order/', create_order, name='create_order'),
    path('send-email/', send_email, name='send_email'),
]
