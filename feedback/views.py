from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Feedback, RatingAnswer, RatingQuestion, OverallAverageRating
from .serializers import FeedbackSerializer, RatingAnswerSerializer, RatingQuestionSerializer, OverallAverageRatingSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Avg
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

def update_all_question_averages():
    """Helper function to update the average rating for all questions."""
    overall_avgs = []
    with transaction.atomic():
        for question in RatingQuestion.objects.all():
            if question.rating_required:
                avg_rating = RatingAnswer.objects.filter(question=question).aggregate(average=Avg('rating'))['average'] or 0
                avg_rating = round(avg_rating, 1)

                # Update or create OverallAverageRating for the question
                overall_avg, _ = OverallAverageRating.objects.get_or_create(question=question)
                overall_avg.average_rating = avg_rating
                overall_avgs.append(overall_avg)

        # Bulk update for efficiency
        OverallAverageRating.objects.bulk_update(overall_avgs, ['average_rating'])

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    def get_permissions(self):
        if self.action == 'create':  # POST request
            permission_classes = [AllowAny]  # Allow any for POST requests (feedback creation)
        else:  # GET, DELETE, etc.
            permission_classes = [IsAuthenticated]  # Require authentication for other methods (like GET, PUT, DELETE)
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            feedback = serializer.save()
            ratings_data = request.data.get('ratings', [])
            rating_answers = []
            errors = []

            for rating_data in ratings_data:
                question_id = rating_data.get('question_id')
                question = get_object_or_404(RatingQuestion, id=question_id)
                rating_value = rating_data.get('rating')  

                rating_answers.append(
                    RatingAnswer(
                        feedback=feedback,
                        question=question,
                        rating=rating_value,  
                        answer=rating_data.get('answer', '')
                    )
                )
            if rating_answers:
                RatingAnswer.objects.bulk_create(rating_answers)
            update_all_question_averages()
            if errors:
                return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        # Recalculate averages for all questions after deletion
        update_all_question_averages()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['patch'], url_path='mark-complete')
    def mark_complete(self, request, pk=None):
        feedback = self.get_object()
        feedback.status = 'complete'
        feedback.save()
        return Response({'status': 'Feedback marked as complete'})

class OverallAverageRatingView(APIView):
    def get(self, request):
        averages = OverallAverageRating.objects.filter(question__rating_required=True)
        serializer = OverallAverageRatingSerializer(averages, many=True)
        return Response(serializer.data)

class RatingQuestionViewSet(viewsets.ModelViewSet):
    queryset = RatingQuestion.objects.all().order_by('id')     
    serializer_class = RatingQuestionSerializer
    permission_classes = [AllowAny] 

    def retrieve(self, request, pk=None):
        question = get_object_or_404(RatingQuestion, pk=pk)
        serializer = self.get_serializer(question)
        return Response(serializer.data)
