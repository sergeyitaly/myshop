from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "products"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('products/', views.ProductList.as_view(), name='products'),
    path('product/<int:pk>/', views.ProductDetail.as_view(), name='product' ),
    path('collections/', views.CollectionList.as_view(), name='collections'),
    path('collection/<int:pk>/', views.CollectionDetail.as_view(), name='collection'),
    path('categories/', views.CategoryList.as_view(), name='categories'),
    path('category/<int:pk>', views.CategoryDetail.as_view(), name='category'),
    path('collection_items/<int:pk>/', views.CollectionItemsPage.as_view(), name='collection_items_page'),

#    path('', views.home, name='home'),  # Map root URL to home_view

]

urlpatterns = format_suffix_patterns(urlpatterns)