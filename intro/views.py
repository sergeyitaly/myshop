from rest_framework import generics
from .models import Intro
from .serializers import IntroSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

class IntroPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10

class IntroListView(generics.ListAPIView):
    queryset = Intro.objects.all()
    serializer_class = IntroSerializer
    pagination_class = IntroPagination
    permission_classes = [AllowAny]

class IntroDetailAPIView(generics.RetrieveAPIView):
    queryset = Intro.objects.all()
    serializer_class = IntroSerializer
    permission_classes = [AllowAny]