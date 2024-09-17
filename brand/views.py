from rest_framework import generics
from .models import Brand
from .serializers import BrandSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

class BrandPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 10

class BrandListView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = BrandPagination
    permission_classes = [AllowAny]

class BrandDetailAPIView(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]
