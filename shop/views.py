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
from django.http import JsonResponse
from django.http import HttpResponse



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

        return queryset
    
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