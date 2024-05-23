from django.urls import path
from .views import create_order

app_name = "orders"

urlpatterns = [
    path('order/', create_order, name='order'),
]