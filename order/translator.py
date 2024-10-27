from modeltranslation.translator import translator, TranslationOptions
from .models import Order

class OrderTranslationOptions(TranslationOptions):
    fields = ('congrats',)  # Assuming Category only needs name translation

translator.register(Order, OrderTranslationOptions)

