import django_filters
from django_filters.rest_framework import OrderingFilter
from .models import Product

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

#was created to allow filtering by multiple numbers using in
class ProductFilter(django_filters.FilterSet):
    # Filter products by category and collection
    category_id = NumberInFilter(field_name='collection__category__id', lookup_expr='in')
    collection_id = NumberInFilter(field_name='collection__id', lookup_expr='in')

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
            'category_id', 'collection_id', 'name', 'name_en', 'name_uk', 
            'price_min', 'price_max', 'sales_count', 'popularity', 'has_discount'
        ]

    def filter_has_discount(self, queryset, name, value):
        """
        Filter the queryset to include only products with a discount if value is True.
        """
        if value:
            return queryset.filter(discount__gt=0)
        return queryset