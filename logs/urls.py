from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('', views.index, name='index'),  # Add your views here
]