# translation.py
from modeltranslation.translator import TranslationOptions, translator
from .models import RatingQuestion, OverallAverageRating

class RatingQuestionTranslationOptions(TranslationOptions):
    fields = ('question', 'aspect_name',)

translator.register(RatingQuestion, RatingQuestionTranslationOptions)
