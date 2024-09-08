from rest_framework import generics
from .models import TeamMember
from .serializers import TeamMemberSerializer
from rest_framework.pagination import PageNumberPagination

class TeamMemberPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10

class TeamMemberListView(generics.ListAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    pagination_class = TeamMemberPagination
