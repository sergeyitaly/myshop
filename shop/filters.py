import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    # Filter products by category name through the collection
    category = django_filters.CharFilter(field_name='collection__category__name', lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    sales_count = django_filters.NumberFilter()
    popularity = django_filters.NumberFilter()

    class Meta:
        model = Product
        fields = ['category', 'name', 'price_min', 'price_max', 'sales_count', 'popularity']
