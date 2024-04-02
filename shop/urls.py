from unicodedata import name
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from shop import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "products"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('products/', views.ProductList.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product' ),
    path('categories/', views.CategoryList.as_view(), name='categories'),
    path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category'),
]

urlpatterns = format_suffix_patterns(urlpatterns)