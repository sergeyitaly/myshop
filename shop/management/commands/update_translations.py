from django.core.management.base import BaseCommand
from django.db import transaction
from modeltranslation.translator import translator
from shop.models import Product, Category, Collection, AdditionalField  # Replace 'yourapp' with your actual app name

class Command(BaseCommand):
    help = 'Copy values from non-translated fields to translated fields with suffixes _uk and _en'

    def handle(self, *args, **options):
        models = [Product, Category, Collection, AdditionalField]
        for model in models:
            self.copy_translations(model)
        self.stdout.write(self.style.SUCCESS('Successfully copied translations.'))

    def copy_translations(self, model):
        translation_options = translator.get_options_for_model(model)
        fields = translation_options.fields
        
        # Get all objects of the model
        objects = model.objects.all()
        
        with transaction.atomic():
            for obj in objects:
                for field in fields:
                    value = getattr(obj, field, None)
                    if value:
                        for lang_code in ['uk', 'en']:
                            translated_field = f"{field}_{lang_code}"
                            if hasattr(obj, translated_field):
                                setattr(obj, translated_field, value)
                        obj.save()
