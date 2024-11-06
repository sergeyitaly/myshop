from django.urls import path
from .views import api_logs_view

urlpatterns = [
    path('logs/', api_logs_view, name='api_logs_view'),
]
