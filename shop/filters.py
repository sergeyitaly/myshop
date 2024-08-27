import django_filters
from django_filters.rest_framework import OrderingFilter
from .models import Product
from django.db.models import Q

class ProductsFilter(django_filters.FilterSet):
    sales_count = django_filters.NumberFilter(field_name='sales_count', lookup_expr='exact')
    popularity = django_filters.NumberFilter(field_name='popularity', lookup_expr='gte')
    price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Product
        fields = ['popularity', 'price', 'sales_count']

    def filter_search(self, queryset, name, value):
        if value:
            search_term = value.lower()
            return queryset.filter(
                Q(name_en__icontains=search_term) | 
                Q(name_uk__icontains=search_term)
            )
        return queryset
    

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class ProductFilter(django_filters.FilterSet):
    # Filter products by category and collection
    category_id = NumberInFilter(field_name='collection__category__id', lookup_expr='in')
    collection_id = NumberInFilter(field_name='collection__id', lookup_expr='in')

    # Filter by translated name fields
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    search = django_filters.CharFilter(method='filter_search')

    
    # Filter by discounted price range
    price_min = django_filters.NumberFilter(
        field_name='discounted_price', 
        lookup_expr='gte'
    )
    price_max = django_filters.NumberFilter(
        field_name='discounted_price', 
        lookup_expr='lte'
    )
    
    # Filter by sales count and popularity
    sales_count = django_filters.NumberFilter(field_name='sales_count', lookup_expr='exact')
    popularity = django_filters.NumberFilter(field_name='popularity', lookup_expr='exact')

    # Filter by products with a discount
    has_discount = django_filters.BooleanFilter(
        field_name='discount', 
        method='filter_has_discount', 
        label='Has Discount'
    )

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
        fields = [
            'category_id', 'collection_id', 'search', 'price_min', 'price_max', 
            'sales_count', 'popularity', 'has_discount'
        ]

    def filter_search(self, queryset, name, value):
        if value:
            search_term = value.lower()
            return queryset.filter(
                Q(name_en__icontains=search_term) | 
                Q(name_uk__icontains=search_term)
            )
        return queryset

    def filter_has_discount(self, queryset, name, value):
        return queryset.filter(discount__gt=0) if value else queryset.filter(discount=0)
