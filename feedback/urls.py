from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeedbackViewSet, OverallAverageRatingView

router = DefaultRouter()
router.register(r'feedback', FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('', include(router.urls)),
    path('average-ratings/', OverallAverageRatingView.as_view(), name='overall-average-ratings'),
]
