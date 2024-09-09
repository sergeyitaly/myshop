from rest_framework import generics
from .models import TeamMember
from .serializers import TeamMemberSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

class TeamMemberPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10

class TeamMemberListView(generics.ListAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    pagination_class = TeamMemberPagination
    permission_classes = [AllowAny]

class TeamMemberDetailAPIView(generics.RetrieveAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [AllowAny]