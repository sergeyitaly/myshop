import django_filters
from django_filters import OrderingFilter
from .models import Product

class ProductFilter(django_filters.FilterSet):
    # Filter products by category name through the collection
    category_id = django_filters.BaseInFilter(field_name='collection__category__id', lookup_expr='in')
    collection_id = django_filters.BaseInFilter(field_name='collection__id', lookup_expr='in')
    name = django_filters.CharFilter(lookup_expr='icontains')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    sales_count = django_filters.NumberFilter()
    popularity = django_filters.NumberFilter()
    
    ordering = OrderingFilter(
        fields=(
            ('popularity', 'popularity'),
            ('-popularity', 'popularity_desc'),
            ('sales_count', 'sales_count'),
            ('-sales_count', 'sales_count_desc'),
            ('discounted_price', 'discounted_price'),
            ('-discounted_price', 'discounted_price_desc'),
            ('price', 'price'),
            ('-price', 'price_desc'),
        ),
        field_labels={
            'popularity': 'Popularity',
            'popularity_desc': 'Popularity (descending)',
            'sales_count': 'Sales Count',
            'sales_count_desc': 'Sales Count (descending)',
            'discounted_price': 'Discounted Price',
            'discounted_price_desc': 'Discounted Price (descending)',
            'price': 'Price',
            'price_desc': 'Price (descending)',
        }
    )

    class Meta:
        model = Product
        fields = ['category_id', 'collection_id', 'name', 'price_min', 'price_max', 'sales_count', 'popularity', 'ordering']
