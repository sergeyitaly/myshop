# urls.py

from django.urls import path
from .views import create_order, send_email  # Import the view function for sending email

app_name = "orders"

urlpatterns = [
    path('order/', create_order, name='order'),
    path('send-email/', send_email, name='send_email'),  # Define the URL endpoint for sending email
]
