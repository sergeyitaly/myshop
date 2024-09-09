from django.urls import path
from .views import TeamMemberListView

urlpatterns = [
    path('team/', TeamMemberListView.as_view(), name='team-member-list'),
]
