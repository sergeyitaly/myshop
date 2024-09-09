from django.urls import path
from .views import *

urlpatterns = [
    path('brand/', BrandListView.as_view(), name='brand-list'),
    path('brand/<int:pk>/', BrandDetailAPIView.as_view(), name='brand-detail'),

]
