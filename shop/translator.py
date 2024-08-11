from modeltranslation.translator import translator, TranslationOptions
from .models import Product, Category, Collection, AdditionalField

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)  # Assuming Category only needs name translation

class CollectionTranslationOptions(TranslationOptions):
    fields = ('name', )  # Assuming Collection has name and description fields

class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'color_value')  # Assuming Product has name, description, and color_value fields

class AdditionalFieldTranslationOptions(TranslationOptions):
    fields = ('name', 'value')  # Assuming AdditionalField has name and value fields

translator.register(Product, ProductTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
translator.register(Collection, CollectionTranslationOptions)
translator.register(AdditionalField, AdditionalFieldTranslationOptions)
