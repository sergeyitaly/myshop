from django.urls import path
from .views import *

urlpatterns = [
    path('team/', TeamMemberListView.as_view(), name='team-member-list'),
    path('team/<int:pk>/', TeamMemberDetailAPIView.as_view(), name='team-member-detail'),

]
