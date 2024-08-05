import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.NumberFilter()
    sales_count = django_filters.NumberFilter()
    popularity = django_filters.NumberFilter()

    class Meta:
        model = Product
        fields = ['category', 'name', 'price', 'sales_count', 'popularity']