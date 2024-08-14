import django_filters
from django_filters import OrderingFilter
from .models import Product

class ProductFilter(django_filters.FilterSet):
    # Filter products by category name through the collection
    category_id = django_filters.BaseInFilter(field_name='collection__category__id', lookup_expr='in')
    collection_id = django_filters.BaseInFilter(field_name='collection__id', lookup_expr='in')
    
    # Filter by translated name fields
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    name_en = django_filters.CharFilter(field_name='name_en', lookup_expr='icontains')
    name_uk = django_filters.CharFilter(field_name='name_uk', lookup_expr='icontains')
    
    # Filter by price range
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    # Filter by sales count and popularity
    sales_count = django_filters.NumberFilter(field_name='sales_count', lookup_expr='exact')
    popularity = django_filters.NumberFilter(field_name='popularity', lookup_expr='exact')
    
    # Ordering
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
        fields = ['category_id', 'collection_id', 'name', 'name_en', 'name_uk', 'price_min', 'price_max', 'sales_count', 'popularity', 'ordering']
