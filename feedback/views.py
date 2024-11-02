from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Feedback, RatingAnswer, RatingQuestion, OverallAverageRating
from .serializers import FeedbackSerializer, RatingAnswerSerializer, RatingQuestionSerializer, OverallAverageRatingSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            feedback = serializer.save()
            ratings_data = request.data.get('ratings', [])
            rating_answers = []
            errors = []

            for rating_data in ratings_data:
                question_id = rating_data.get('question_id')
                if question_id is None:
                    errors.append("Missing 'question_id' in rating data.")
                    continue

                question = get_object_or_404(RatingQuestion, id=question_id)
                if question.rating_required:
                    rating = rating_data.get('rating')
                    if rating is None:
                        errors.append(f"Missing 'rating' for required question (ID: {question_id})")
                        continue
                    rating_answers.append(
                        RatingAnswer(feedback=feedback, question=question, rating=rating, answer=rating_data.get('answer', ''))
                    )
                else:
                    logger.info(f"Skipped rating for question (ID: {question_id}): rating not required.")

            # Bulk create ratings only if there are valid entries
            if rating_answers:
                RatingAnswer.objects.bulk_create(rating_answers)

            if errors:
                return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Endpoint for marking feedback as complete
    @action(detail=True, methods=['patch'], url_path='mark-complete')
    def mark_complete(self, request, pk=None):
        feedback = self.get_object()
        feedback.status = 'complete'
        feedback.save()
        return Response({'status': 'Feedback marked as complete'})

class OverallAverageRatingView(APIView):
    def get(self, request):
        # Calculate overall averages (if necessary)
        OverallAverageRating.calculate_overall_averages()        
        # Filter averages to only include those where the associated RatingQuestion requires a rating
        averages = OverallAverageRating.objects.filter(question__rating_required=True)
        # Serialize the filtered averages
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