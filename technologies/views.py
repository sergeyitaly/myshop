from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

class TechnologyPagination(PageNumberPagination):
    page_size = 20                
    page_size_query_param = 'page_size'
    max_page_size = 24

class TechnologyListView(generics.ListAPIView):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    pagination_class = TechnologyPagination
    permission_classes = [AllowAny]

class TechnologyDetailAPIView(generics.RetrieveAPIView):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    permission_classes = [AllowAny]