from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeedbackViewSet, OverallAverageRatingView, RatingQuestionViewSet

router = DefaultRouter()
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'rating-questions', RatingQuestionViewSet, basename='rating-questions')  # Register RatingQuestionViewSet

urlpatterns = [
    path('', include(router.urls)),
    path('average-ratings/', OverallAverageRatingView.as_view(), name='overall-average-ratings'),
]
