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
from django.db.models import Min, Max
from django.db.models import F, FloatField, ExpressionWrapper, Min, Max


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
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'sales_count', 'popularity']
    
class ProductListFilter(generics.ListAPIView):
    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price', 'popularity', 'sales_count']
    ordering = ['-discounted_price']  # Default ordering

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Annotate with discounted price
        queryset = queryset.annotate(
            discounted_price=ExpressionWrapper(
                F('price') * (1 - F('discount') / 100.0),
                output_field=FloatField()
            )
        )

        # Retrieve price range parameters
        price_min = self.request.query_params.get('price_min', None)
        price_max = self.request.query_params.get('price_max', None)
        
        # Calculate default min and max price if not provided
        if price_min is None or price_max is None:
            price_range = queryset.aggregate(min_price=Min('discounted_price'), max_price=Max('discounted_price'))
            if price_min is None:
                price_min = price_range['min_price']
            if price_max is None:
                price_max = price_range['max_price']
        
        # Filter queryset based on provided price range
        queryset = queryset.filter(discounted_price__gte=price_min, discounted_price__lte=price_max)

        # Handle custom ordering parameters
        ordering = self.request.query_params.get('ordering', '-discounted_price')
        
        # Handle valid ordering fields
        valid_ordering_fields = {
            'popularity_up': 'popularity',
            'popularity_down': '-popularity',
            'sales_count_up': 'sales_count',
            'sales_count_down': '-sales_count',
            'price_up': 'discounted_price',
            'price_down': '-discounted_price'
        }
        
        if ordering in valid_ordering_fields:
            ordering = valid_ordering_fields[ordering]
        else:
            ordering = '-discounted_price'  # Default ordering
        
        return queryset.order_by(ordering)

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
