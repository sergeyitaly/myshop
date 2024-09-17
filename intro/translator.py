from modeltranslation.translator import TranslationOptions,translator, TranslationOptions
from .models import Intro

class IntroTranslationOptions(TranslationOptions):
    fields = ('name','description')

translator.register(Intro, IntroTranslationOptions)
