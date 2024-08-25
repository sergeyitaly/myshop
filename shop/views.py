from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from .serializers import ProductSerializer, CollectionSerializer, CategorySerializer
from .models import Product, Collection, Category
from .filters import ProductFilter, ProductsFilter
from django.db.models import F, FloatField, ExpressionWrapper, Min, Max, Q
from django.core.cache import cache
from rest_framework import generics, permissions
from .models import AdditionalField
from .serializers import AdditionalFieldSerializer
from rest_framework.filters import SearchFilter
from django.http import FileResponse, Http404
from django.conf import settings
import os
from django.utils import timezone
from datetime import timedelta
from django.utils.cache import add_never_cache_headers
import urllib.parse

class LargePageNumberPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100

class CustomPageNumberPagination(PageNumberPagination):
    default_page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data,
            'next_page_number': self.page.number + 1 if self.page.has_next() else None,
            'previous_page_number': self.page.number - 1 if self.page.has_previous() else None,
            'page_size': self.page.paginator.per_page,
        })

class CollectionPageNumberPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data,
            'next_page_number': self.page.number + 1 if self.page.has_next() else None,
            'previous_page_number': self.page.number - 1 if self.page.has_previous() else None,
            'page_size': self.page.paginator.per_page,
        })
    
class CachedQueryMixin:
    def get_cached_queryset(self, cache_key, queryset, timeout=60 * 15):
        cached_data = cache.get(cache_key)
        if not cached_data:
            cached_data = queryset
            cache.set(cache_key, cached_data, timeout)
        return cached_data
    
class ProductList(generics.ListCreateAPIView, CachedQueryMixin):
#    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filterset_class = ProductsFilter
    pagination_class = LargePageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name_en', 'name_uk']
    ordering_fields = ['name_en', 'name_uk']

    def get_queryset(self):
        cache_key = f"product_list_{self.request.GET.urlencode()}"
        queryset = Product.objects.all()

        search_query = self.request.query_params.get('search', None)
        if search_query:
            search_query = urllib.parse.unquote(search_query)
            queryset = queryset.filter(
                Q(name_en__icontains=search_query) |
                Q(name_uk__icontains=search_query)
            )

        # Apply filters and ordering
        queryset = self.filter_queryset(queryset)
        
        # Cache the queryset
        cache.set(cache_key, queryset, timeout=60*15)  # Cache for 15 minutes
        
        return queryset



class ProductListFilter(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name_en', 'name_uk']
    pagination_class = LargePageNumberPagination 

    def get_cached_queryset(self, cache_key, queryset):
        """
        Retrieve the cached queryset if available, otherwise set the cache.
        """
        cached_queryset = cache.get(cache_key)
        if not cached_queryset:
            cache.set(cache_key, queryset, timeout=300)  # Cache timeout set to 300 seconds (5 minutes)
            cached_queryset = queryset
        return cached_queryset
    
    def get_queryset(self):
        queryset = Product.objects.all()
        # Apply search filter
        cache_key = f"filtered_product_list_{self.request.GET.urlencode()}"

        search_query = self.request.query_params.get('search', None)
        if search_query:
            search_query = urllib.parse.unquote(search_query)
            queryset = queryset.filter(
                Q(name_en__icontains=search_query) |
                Q(name_uk__icontains=search_query)
            )
        
        # Explicitly filter by collections if provided
        collection_ids = self.request.query_params.get('collection', None)
        if collection_ids:
            collection_ids_list = [int(c) for c in collection_ids.split(',') if c.isdigit()]
            if collection_ids_list:
                queryset = queryset.filter(collection__id__in=collection_ids_list)

        # Explicitly filter by categories if provided
        category_ids = self.request.query_params.get('category', None)
        if category_ids:
            category_ids_list = [int(c) for c in category_ids.split(',') if c.isdigit()]
            if category_ids_list:
                queryset = queryset.filter(collection__category__id__in=category_ids_list)

        # Apply the has_discount filter if provided
        has_discount = self.request.query_params.get('has_discount', None)
        if has_discount is not None:
            if has_discount.lower() in ['true', '1']:
                queryset = queryset.filter(discount__gt=0)  # Only products with a discount
            elif has_discount.lower() in ['false', '0']:
                queryset = queryset.filter(discount=0)  # Only products without a discount

        # Annotate discounted_price
        queryset = queryset.annotate(
            discounted_price=ExpressionWrapper(
                F('price') * (1 - F('discount') / 100.0),
                output_field=FloatField()
            )
        )

        # Default behavior if no specific parameter for price_min or price_max is provided
        queryset = self.filterset_class(self.request.GET, queryset=queryset).qs

        # Ordering logic with multiple fields
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            ordering_fields = ordering.split(',')
            valid_ordering_fields = [
                'discounted_price', '-discounted_price', 
                'price', '-price', 
                'sales_count', '-sales_count', 
                'popularity', '-popularity'
            ]
            # Validate each ordering field
            valid_ordering_fields = [field for field in ordering_fields if field in valid_ordering_fields]
            if valid_ordering_fields:
                queryset = queryset.order_by(*valid_ordering_fields)

        return self.get_cached_queryset(cache_key, queryset)
    
    def list(self, request, *args, **kwargs):
        # Get the filtered queryset
        queryset = self.get_queryset()
        
        # Paginate the queryset
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        
        # Calculate minimum and maximum price considering discount
        discounted_price_min = queryset.aggregate(min_price=Min('discounted_price'))['min_price']
        discounted_price_max = queryset.aggregate(max_price=Max('discounted_price'))['max_price']
        
        # Overall price range calculation
        overall_discounted_price_min = Product.objects.annotate(
            discounted_price=ExpressionWrapper(
                F('price') * (1 - F('discount') / 100.0),
                output_field=FloatField()
            )
        ).aggregate(min_price=Min('discounted_price'))['min_price']
        
        overall_discounted_price_max = Product.objects.annotate(
            discounted_price=ExpressionWrapper(
                F('price') * (1 - F('discount') / 100.0),
                output_field=FloatField()
            )
        ).aggregate(max_price=Max('discounted_price'))['max_price']

        # Serialize the data
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = {
                'price_min': discounted_price_min or 0,
                'price_max': discounted_price_max or 0,
                'overall_price_min': overall_discounted_price_min or 0,
                'overall_price_max': overall_discounted_price_max or 0,
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'count': paginator.page.paginator.count,
                'results': serializer.data,
            }
            return Response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = {
            'price_min': discounted_price_min or 0,
            'price_max': discounted_price_max or 0,
            'overall_price_min': overall_discounted_price_min or 0,
            'overall_price_max': overall_discounted_price_max or 0,
            'count': queryset.count(),
            'results': serializer.data,
        }
        return Response(data)

class CollectionItemsFilterPage(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        collection_id = self.kwargs.get('pk')
        queryset = Product.objects.filter(collection__id=collection_id)
        return queryset

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def perform_update(self, serializer):
        instance = serializer.save()
        # Invalidate the cache when a collection is updated
        cache.delete('product_detail')
        return instance

class CollectionList(generics.ListCreateAPIView, CachedQueryMixin):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [AllowAny]
    pagination_class = LargePageNumberPagination 
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name_en', 'name_uk']
    ordering_fields = ['name_en', 'name_uk']

    def get_queryset(self):
        cache_key = f"collection_list_{self.request.GET.urlencode()}"
        queryset = Collection.objects.only('name_en', 'name_uk')  # Optimize data fetching
        search_query = self.request.query_params.get('search', None)
        if search_query:
            search_query = urllib.parse.unquote(search_query)
            queryset = queryset.filter(
                Q(name_en__icontains=search_query) |
                Q(name_uk__icontains=search_query)
            )
        return self.get_cached_queryset(cache_key, queryset)        
    
    def perform_create(self, serializer):
        instance = serializer.save()
        # Invalidate the cache when a new collection is created
        cache.delete('collection_list')
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        # Invalidate the cache when a collection is updated
        cache.delete('collection_list')
        return instance


class CollectionItemsPage(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination  # Use custom pagination for products
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name_en', 'name_uk']
    ordering_fields = ['name_en', 'name_uk','price']
    permission_classes = [AllowAny]

    def get_queryset(self):
        try:
            collection_id = self.kwargs.get('pk')
            if collection_id is not None:
                collection = Collection.objects.get(pk=collection_id)
                queryset = collection.product_set.all()
            else:
                queryset = Product.objects.none()
        except Collection.DoesNotExist:
            queryset = Product.objects.none()

        return queryset

class CollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [AllowAny]
    
    def perform_update(self, serializer):
        instance = serializer.save()
        # Invalidate the cache when a collection is updated
        cache.delete('collection_list')
        return instance

class CategoryList(generics.ListCreateAPIView, CachedQueryMixin):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name_en', 'name_uk']

    def get_queryset(self):
        cache_key = "category_list"
        queryset = Category.objects.all()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            search_query = urllib.parse.unquote(search_query)
            queryset = queryset.filter(
                Q(name_en__icontains=search_query) |
                Q(name_uk__icontains=search_query)
            )
        return self.get_cached_queryset(cache_key, queryset)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class ProductView(APIView):
    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        response = Response(serializer.data)
        add_never_cache_headers(response)
        return response
    
class AdditionalFieldListCreateView(generics.ListCreateAPIView):
    queryset = AdditionalField.objects.all()
    serializer_class = AdditionalFieldSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class AdditionalFieldDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdditionalField.objects.all()
    serializer_class = AdditionalFieldSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        instance = serializer.save()
        # Invalidate the cache for this specific additional field detail
        cache_key = f"additional_field_detail_{instance.id}"
        cache.delete(cache_key)
        return instance

def serve_image(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(file_path):
        raise Http404("Image not found")
    
    response = FileResponse(open(file_path, 'rb'), content_type='image/jpeg')
    
    # Set cache headers with timezone-aware datetime
    response['Cache-Control'] = 'public, max-age=86400'  # Cache for 1 day
    expires_at = timezone.now() + timedelta(days=1)
    response['Expires'] = expires_at.strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    return response