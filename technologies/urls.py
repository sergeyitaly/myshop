from django.urls import path
from .views import *

urlpatterns = [
    path('technology/', TechnologyListView.as_view(), name='technology-list'),
    path('technology/<int:pk>/', TechnologyDetailAPIView.as_view(), name='technology-detail'),

]
