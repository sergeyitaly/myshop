from unicodedata import name
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "products"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('products/', views.ProductList.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product' ),
    path('collections/', views.CollectionList.as_view(), name='collection'),
    path('collection/<int:pk>/', views.CollectionDetail.as_view(), name='collection'),
]

urlpatterns = format_suffix_patterns(urlpatterns)