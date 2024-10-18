from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Feedback, RatingAnswer, RatingQuestion, OverallAverageRating
from .serializers import FeedbackSerializer, RatingAnswerSerializer, RatingQuestionSerializer, OverallAverageRatingSerializer
from rest_framework.views import APIView

# Feedback ViewSet for creating and listing feedback
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def create(self, request, *args, **kwargs):
        feedback_data = request.data
        serializer = self.get_serializer(data=feedback_data)
        if serializer.is_valid():
            feedback = serializer.save()
            
            # Handle ratings in the feedback
            ratings_data = feedback_data.get('ratings', [])
            for rating_data in ratings_data:
                question = get_object_or_404(RatingQuestion, id=rating_data['question'])
                RatingAnswer.objects.create(
                    feedback=feedback,
                    question=question,
                    rating=rating_data['rating'],
                    answer=rating_data.get('answer', '')
                )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Endpoint for marking feedback as complete
    @action(detail=True, methods=['patch'], url_path='mark-complete')
    def mark_complete(self, request, pk=None):
        feedback = self.get_object()
        feedback.status = 'complete'
        feedback.save()
        return Response({'status': 'Feedback marked as complete'})

# View for retrieving and calculating the overall average rating
class OverallAverageRatingView(APIView):
    def get(self, request):
        OverallAverageRating.calculate_overall_averages()
        averages = OverallAverageRating.objects.all()
        serializer = OverallAverageRatingSerializer(averages, many=True)
        return Response(serializer.data)

# View for listing all rating questions
class RatingQuestionViewSet(viewsets.ModelViewSet):
    queryset = RatingQuestion.objects.all()
    serializer_class = RatingQuestionSerializer
