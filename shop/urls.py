from django.urls import path
from . import views
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns


app_name = "products"
urlpatterns = [
    path('products/', views.ProductList.as_view(), name='products'),
    path('product/<int:pk>/', views.ProductDetail.as_view(), name='product' ),
    path('product/<str:id_name>/', ProductDetail.as_view(), name='product-detail-by-id-name'),
    path('collections/', views.CollectionList.as_view(), name='collection-list'),
    path('collection/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),
    path('categories/', views.CategoryList.as_view(), name='categories'),
    path('category/<int:pk>', views.CategoryDetail.as_view(), name='category'),
    path('collection/<int:pk>/products/', views.CollectionItemsPage.as_view(), name='collection_products'),
    path('products/filter/', ProductListFilter.as_view(), name='product-list-filter'),
    path('collection/<int:pk>/filter/', CollectionItemsFilterPage.as_view(), name='collection_filtered_products'),
#    path('', views.home, name='home'),  # Map root URL to home_view

] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = format_suffix_patterns(urlpatterns)



