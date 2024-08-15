from rest_framework import generics, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from django_filters import FilterSet, NumberFilter
from .serializers import ProductSerializer, CollectionSerializer, CategorySerializer
from .models import Product, Collection, Category
from .filters import ProductFilter
from django.db.models import F, FloatField, ExpressionWrapper, Min, Max, Q
from django.core.cache import cache
from rest_framework import generics, permissions
from .models import AdditionalField
from .serializers import AdditionalFieldSerializer

class CustomPageNumberPagination(PageNumberPagination):
    default_page_size = 4
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
    
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination  # Use custom pagination for products
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'sales_count', 'popularity']


class ProductListFilter(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']

    def get_queryset(self):
        queryset = Product.objects.all()

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

        # Apply price range filter if provided
        price_min = self.request.query_params.get('price_min', None)
        price_max = self.request.query_params.get('price_max', None)
        if price_min and price_min.isdigit():
            queryset = queryset.filter(price__gte=float(price_min))
        if price_max and price_max.isdigit():
            queryset = queryset.filter(price__lte=float(price_max))

        # Annotate discounted_price
        queryset = queryset.annotate(
            discounted_price=ExpressionWrapper(
                F('price') * (1 - F('discount') / 100.0),
                output_field=FloatField()
            )
        )

        # Apply additional filters from filterset_class
        queryset = self.filterset_class(self.request.GET, queryset=queryset).qs

        # Handle ordering based on query parameters
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            ordering_fields = ordering.split(',')
            order_by_fields = []

            for field in ordering_fields:
                if field in ['discounted_price', '-discounted_price']:
                    order_by_fields.append(field)
                elif field == 'price':
                    order_by_fields.append('discounted_price')
                elif field == '-price':
                    order_by_fields.append('-discounted_price')
                else:
                    order_by_fields.append(field)

            if order_by_fields:
                queryset = queryset.order_by(*order_by_fields)

        return queryset
 

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

class CollectionList(generics.ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [AllowAny]
    pagination_class = CollectionPageNumberPagination  # Use custom pagination for collections
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name']
    ordering_fields = ['name']

    
    def get_queryset(self):
        # Cache key for the queryset
        cache_key = 'collection_list'
        # Check if the queryset is already cached
        queryset = cache.get(cache_key)
        
        if not queryset:
            # If not cached, fetch the data and cache it
            queryset = Collection.objects.select_related('category').all()
            cache.set(cache_key, queryset, timeout=60 * 15)  # Cache timeout of 15 minutes
        
        return queryset
    
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
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price']
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

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination  # Use custom pagination for categories
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class ProductView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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