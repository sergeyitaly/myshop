from modeltranslation.translator import TranslationOptions,translator, TranslationOptions
from .models import *

class TechnologyTranslationOptions(TranslationOptions):
    fields = ('name','description')

translator.register(Technology, TechnologyTranslationOptions)
