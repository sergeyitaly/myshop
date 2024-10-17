from rest_framework import viewsets, generics
from rest_framework.response import Response
from .models import Feedback, OverallAverageRating
from .serializers import FeedbackSerializer, OverallAverageRatingSerializer
from rest_framework.permissions import IsAuthenticated

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Save the feedback and trigger the calculation of overall average ratings."""
        serializer.save()
        # Recalculate overall averages when new feedback is created
        OverallAverageRating.calculate_overall_averages()


class OverallAverageRatingView(generics.RetrieveAPIView):
    """Retrieve the overall average ratings across all feedback."""
    queryset = OverallAverageRating.objects.all()
    serializer_class = OverallAverageRatingSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the first (and only) instance of OverallAverageRating
        return OverallAverageRating.objects.first()
