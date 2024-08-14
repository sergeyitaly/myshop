from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from shop.models import Collection
import os

class Command(BaseCommand):
    help = 'Validate image URLs for collections'

    def handle(self, *args, **kwargs):
        collections = Collection.objects.all()
        for collection in collections:
            photo_url = collection.photo.url if collection.photo else 'No photo'
            thumbnail_path = os.path.join('media', 'CACHE', 'images', 'photos', 'collection', collection.photo.name)
            
            if default_storage.exists(thumbnail_path):
                self.stdout.write(self.style.SUCCESS(f'Thumbnail exists: {thumbnail_path}'))
            else:
                self.stdout.write(self.style.ERROR(f'Thumbnail missing: {thumbnail_path}'))
            
            self.stdout.write(f'Generated photo URL: {photo_url}')
