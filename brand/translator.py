from modeltranslation.translator import TranslationOptions,translator, TranslationOptions
from .models import Brand

class BrandTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Brand, BrandTranslationOptions)
