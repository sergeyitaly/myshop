from django.urls import path
from .views import BrandListView

urlpatterns = [
    path('brand/', BrandListView.as_view(), name='brand-list'),
]
