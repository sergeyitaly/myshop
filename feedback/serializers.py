from rest_framework import serializers
from .models import RatingQuestion, Feedback, RatingAnswer, OverallAverageRating
import logging
from django.db import transaction

logger = logging.getLogger(__name__)


# Serializer for RatingQuestion
class RatingQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingQuestion
        fields = ['id','question','question_en', 'question_uk', 'aspect_name', 'aspect_name_en', 'aspect_name_uk', 'rating_required']

# Serializer for RatingAnswer
class RatingAnswerSerializer(serializers.ModelSerializer):
    question = RatingQuestionSerializer(read_only=True)
    question_id = serializers.PrimaryKeyRelatedField(queryset=RatingQuestion.objects.all(), write_only=True, source='question')

    class Meta:
        model = RatingAnswer
        fields = ['id', 'question', 'question_id', 'answer', 'rating']

class FeedbackSerializer(serializers.ModelSerializer):
    ratings = RatingAnswerSerializer(many=True, write_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'name', 'comment', 'email', 'created_at', 'status', 'ratings']

    def create(self, validated_data):
        ratings_data = validated_data.pop('ratings', [])
        logger.debug("Received feedback data: %s", validated_data)  # Log the main feedback data
        logger.debug("Received ratings data: %s", ratings_data)  # Log the ratings data
        feedback = Feedback.objects.create(**validated_data)
        ratings_to_create = []
        question_ids = {rating['question_id'] for rating in ratings_data if 'question_id' in rating}
        rating_questions = {question.id: question for question in RatingQuestion.objects.filter(id__in=question_ids)}

        for rating_data in ratings_data:
            question_id = rating_data.get('question_id')
            if question_id in rating_questions:
                rating_question = rating_questions[question_id]
                if rating_question.rating_required or 'rating' in rating_data:
                    ratings_to_create.append(RatingAnswer(feedback=feedback, **rating_data))
                else:
                    logger.warning("Rating not provided for non-required question ID %s", question_id)
            else:
                logger.error("RatingQuestion with ID %s does not exist", question_id)

        if ratings_to_create:
            RatingAnswer.objects.bulk_create(ratings_to_create)

        return feedback
    
    def update(self, instance, validated_data):
        ratings_data = validated_data.pop('ratings', None)
        instance.name = validated_data.get('name', instance.name)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.email = validated_data.get('email', instance.email)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        if ratings_data:
            for rating_data in ratings_data:
                question_id = rating_data.get('question_id')
                if question_id:
                    try:
                        rating_question = RatingQuestion.objects.get(id=question_id)
                        rating_answer = RatingAnswer.objects.filter(feedback=instance, question=rating_question).first()
                        if rating_answer:
                            # Update existing rating answer if the question requires it
                            if rating_question.rating_required:
                                rating_answer.rating = rating_data.get('rating', rating_answer.rating)
                                rating_answer.answer = rating_data.get('answer', rating_answer.answer)
                                rating_answer.save()
                        else:
                            # Create new rating answer if it does not exist
                            if rating_question.rating_required or 'rating' in rating_data:
                                RatingAnswer.objects.create(feedback=instance, **rating_data)
                            else:
                                logger.warning("Rating not provided for non-required question ID %s", question_id)
                    except RatingQuestion.DoesNotExist:
                        logger.error("RatingQuestion with ID %s does not exist", question_id)

        return instance

class OverallAverageRatingSerializer(serializers.ModelSerializer):
    model = OverallAverageRating
    question = RatingQuestionSerializer(read_only=True)

    class Meta:
        model = OverallAverageRating
        fields = ['question', 'average_rating']
