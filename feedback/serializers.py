from rest_framework import serializers
from .models import RatingQuestion, Feedback, RatingAnswer, OverallAverageRating
import logging

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


# Serializer for Feedback
class FeedbackSerializer(serializers.ModelSerializer):
    ratings = RatingAnswerSerializer(many=True, write_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'name', 'comment', 'email', 'created_at', 'status', 'ratings']

    def create(self, validated_data):
        # Handle nested RatingAnswer creation
        ratings_data = validated_data.pop('ratings', [])
        logger.debug("Received feedback data: %s", validated_data)  # Log the main feedback data
        logger.debug("Received ratings data: %s", ratings_data)  # Log the ratings data

        # Create the feedback instance
        feedback = Feedback.objects.create(**validated_data)

        # Create RatingAnswer instances
        for rating_data in ratings_data:
            try:
                RatingAnswer.objects.create(feedback=feedback, **rating_data)
            except Exception as e:
                logger.error("Error creating RatingAnswer for feedback ID %s: %s", feedback.id, e)

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
                rating_answer = RatingAnswer.objects.filter(feedback=instance, question=question_id).first()
                if rating_answer:
                    rating_answer.rating = rating_data.get('rating', rating_answer.rating)
                    rating_answer.answer = rating_data.get('answer', rating_answer.answer)
                    rating_answer.save()
                else:
                    RatingAnswer.objects.create(feedback=instance, **rating_data)

        return instance

class OverallAverageRatingSerializer(serializers.ModelSerializer):
    model = OverallAverageRating
    question = RatingQuestionSerializer(read_only=True)

    class Meta:
        model = OverallAverageRating
        fields = ['question', 'average_rating']
