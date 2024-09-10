from django.urls import path
from .views import *

urlpatterns = [
    path('intro/', IntroListView.as_view(), name='intro-list'),
    path('intro/<int:pk>/', IntroDetailAPIView.as_view(), name='intro-detail'),

]
