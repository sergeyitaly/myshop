from rest_framework import viewsets, generics
from rest_framework.response import Response
from .models import Feedback, OverallAverageRating
from .serializers import FeedbackSerializer, OverallAverageRatingSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """Save the feedback and trigger the calculation of overall average ratings."""
        serializer.save(status='processed')
        # Recalculate overall averages when new feedback is created
        OverallAverageRating.calculate_overall_averages()


    # Dynamic permission assignment based on the action (e.g., 'create' or 'list')
    def get_permissions(self):
        if self.action == 'create':
            # Allow anyone to create a comment
            return [AllowAny()]
        # Require authentication for other actions (list, retrieve, update, etc.)
        return [IsAuthenticated()]

class OverallAverageRatingView(generics.RetrieveAPIView):
    """Retrieve the overall average ratings across all feedback."""
    queryset = OverallAverageRating.objects.all()
    serializer_class = OverallAverageRatingSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the first (and only) instance of OverallAverageRating
        return OverallAverageRating.objects.first()
