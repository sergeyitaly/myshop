from modeltranslation.translator import TranslationOptions,translator, TranslationOptions
from .models import Feedback

class FeedbackTranslationOptions(TranslationOptions):
    fields = ('question1', 'question2',
             'question3', 'question4', 
             'question5', 'question6', 
             'question7','question8',
             'question9','question10', )

translator.register(Feedback, FeedbackTranslationOptions)
