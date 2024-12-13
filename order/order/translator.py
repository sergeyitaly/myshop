from modeltranslation.translator import translator, TranslationOptions
from .models import Order, OrderItem

class OrderTranslationOptions(TranslationOptions):
    fields = ('congrats',)  # If only 'congrats' needs translation

class OrderItemTranslationOptions(TranslationOptions):
    # Do not include the foreign key itself, translate fields within the related model
    pass  # No need to include 'product' here

translator.register(Order, OrderTranslationOptions)
translator.register(OrderItem, OrderItemTranslationOptions)
