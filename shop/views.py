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
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.throttling import UserRateThrottle
from django.utils.encoding import uri_to_iri

class ListPageNumberPagination(PageNumberPagination):
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
    
class CustomPageNumberPagination(PageNumberPagination):
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
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filterset_class = ProductsFilter
    pagination_class = ListPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name_en', 'name_uk']
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'search'
    ordering_fields = ['id_name'] 
    
    def get_queryset(self):
        cache_key = 'product_list'
        queryset = self.get_cached_queryset(cache_key, Product.objects.all())

        queryset = queryset.select_related('collection').prefetch_related('productimage_set').defer('additionalfield','description','created', 'updated', 'slug')

        search_query = self.request.query_params.get('search')
        if search_query:
            search_query = uri_to_iri(search_query)  # Decode URL-encoded search query
            queryset = queryset.filter(
                Q(name_en__icontains=search_query) |
                Q(name_uk__icontains=search_query)
            )

        return self.filter_queryset(queryset)

    def perform_create(self, serializer):
        instance = serializer.save()
        cache.delete('product_list')
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        cache.delete('product_list')
        return instance

class ProductListFilter(generics.ListCreateAPIView, CachedQueryMixin):
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name_en', 'name_uk']
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'products'
    ordering_fields = ['id_name']

    def get_queryset(self):
        # Build the base queryset
        queryset = Product.objects.annotate(
            discounted_price=ExpressionWrapper(
                F('price') * (1 - F('discount') / 100.0),
                output_field=FloatField()
            )
        )
        queryset = queryset.select_related('collection', 'collection__category').prefetch_related('productimage_set').defer('additionalfield','description','created', 'updated', 'slug')

        # Apply filters
        collection_ids = self.request.query_params.get('collection', None)
        if collection_ids:
            collection_ids_list = [int(c) for c in collection_ids.split(',') if c.isdigit()]
            queryset = queryset.filter(collection__id__in=collection_ids_list)

        category_ids = self.request.query_params.get('category', None)
        if category_ids:
            category_ids_list = [int(c) for c in category_ids.split(',') if c.isdigit()]
            queryset = queryset.filter(collection__category__id__in=category_ids_list)

        has_discount = self.request.query_params.get('has_discount', None)
        if has_discount is not None:
            if has_discount.lower() in ['true', '1']:
                queryset = queryset.filter(discount__gt=0)
            elif has_discount.lower() in ['false', '0']:
                queryset = queryset.filter(discount=0)

        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        if price_min and price_max:
            queryset = queryset.filter(discounted_price__gte=price_min, discounted_price__lte=price_max)

        # Apply filters from filterset_class
        if any(param in self.request.query_params for param in ['collection', 'category', 'has_discount', 'price_min', 'price_max']):
            queryset = self.filter_queryset(queryset)
        # Handle ordering
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            ordering_fields = ordering.split(',')
            valid_ordering_fields = [
                'discounted_price', '-discounted_price', 
                'price', '-price', 
                'sales_count', '-sales_count', 
                'popularity', '-popularity'
            ]
            valid_ordering_fields = [field for field in ordering_fields if field in valid_ordering_fields]
            if valid_ordering_fields:
                queryset = queryset.order_by(*valid_ordering_fields)

        return queryset

    def list(self, request, *args, **kwargs):
        # Get the filtered queryset
        queryset = self.get_queryset()

        # Calculate the discounted price range (min/max)
        discounted_price_min = queryset.aggregate(min_price=Min('discounted_price'))['min_price']
        discounted_price_max = queryset.aggregate(max_price=Max('discounted_price'))['max_price']

        # Cache the results for price range if not already cached
        overall_discounted_price_min = cache.get('overall_discounted_price_min')
        overall_discounted_price_max = cache.get('overall_discounted_price_max')

        if overall_discounted_price_min is None or overall_discounted_price_max is None:
            overall_discounted_price_min = queryset.aggregate(min_price=Min('discounted_price'))['min_price']
            overall_discounted_price_max = queryset.aggregate(max_price=Max('discounted_price'))['max_price']
            
            cache.set('overall_discounted_price_min', overall_discounted_price_min, timeout=60 * 15)
            cache.set('overall_discounted_price_max', overall_discounted_price_max, timeout=60 * 15)

        # Paginate the queryset
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)

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
    lookup_field = 'id_name'

    def get_object(self):
        id = self.kwargs.get('id')
        id_name = self.kwargs.get('id_name')
        if id is not None:
            product = Product.objects.filter(id=id).first()
            if product:
                return product
        if id_name:
            product = Product.objects.filter(id_name=id_name).first()
            if product:
                return product
        raise Http404("Product not found")

    def perform_update(self, serializer):
        instance = serializer.save()
        # Invalidate the cache when a collection is updated
        cache.delete('product_detail')
        return instance

class CollectionList(generics.ListCreateAPIView, CachedQueryMixin):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [AllowAny]
    pagination_class = CollectionPageNumberPagination 
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name']
#    ordering_fields = ['name_en', 'name_uk']
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'collections'  # Use the defined throttle scope
    ordering_fields = ['name_en', 'name_uk']
#    def get_queryset(self):
#        queryset = Collection.objects.only('name')  # Optimize data fetching
#        search_query = self.request.query_params.get('search', None)
#        if search_query:
#            search_query = urllib.parse.unquote(search_query)
#            queryset = queryset.filter(
#                Q(name_en__icontains=search_query) |
#                Q(name_uk__icontains=search_query)
#            )
#        return queryset       
    
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
            queryset = Product.objects.filter(collection__id=collection_id) \
                .select_related('collection') \
                .prefetch_related('productimage_set')
            if collection_id is not None:
                collection = Collection.objects.get(pk=collection_id)
                queryset = collection.product_set.only('name_en', 'name_uk')
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
    search_fields = ['name']

    def get_queryset(self):
        queryset = Category.objects.only('name')
        search_query = self.request.query_params.get('search', None)
        if search_query:
            search_query = urllib.parse.unquote(search_query)
            queryset = queryset.filter(
                Q(name_en__icontains=search_query) |
                Q(name_uk__icontains=search_query)
            )
        return queryset


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class ProductView(APIView):
    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        # Ensure product availability is updated
        if product.stock == 0:
            product.available = False
        else:
            product.available = True
        product.save(update_fields=["available"]) 
        
        serializer = ProductSerializer(product)
        response_data = serializer.data
        response_data["availability_message"] = (
            "Out of stock" if not product.available else "In stock"
        )
        
        response = Response(response_data)
        add_never_cache_headers(response)
        return response
    
class AdditionalFieldListCreateView(generics.ListCreateAPIView):
    queryset = AdditionalField.objects.all()
    serializer_class = AdditionalFieldSerializer
    permission_classes = [AllowAny]


class AdditionalFieldDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdditionalField.objects.all()
    serializer_class = AdditionalFieldSerializer
    permission_classes = [AllowAny]

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