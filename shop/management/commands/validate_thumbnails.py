from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from shop.models import Collection
from PIL import Image
import os
from io import BytesIO

class Command(BaseCommand):
    help = 'Validate and generate thumbnails for collection images'

    def handle(self, *args, **kwargs):
        collections = Collection.objects.all()
        for collection in collections:
            if collection.photo:
                photo_path = collection.photo.path
                photo_url = collection.photo.url
                
                # Define paths
                thumbnail_path = os.path.join('media', 'CACHE', 'images', 'photos', 'collection', collection.photo.name)
                thumbnail_dir = os.path.dirname(thumbnail_path)

                # Check if the original image exists
                if default_storage.exists(photo_path):
                    self.stdout.write(f'Processing image: {photo_path}')
                    
                    # Check if the thumbnail already exists
                    if not default_storage.exists(thumbnail_path):
                        self.stdout.write(f'Thumbnail missing: {thumbnail_path}')
                        self.create_thumbnail(photo_path, thumbnail_path, thumbnail_dir)
                    
                    self.stdout.write(f'Generated photo URL: {photo_url}')
                else:
                    self.stdout.write(f'Original image not found: {photo_path}')

    def create_thumbnail(self, photo_path, thumbnail_path, thumbnail_dir):
        # Create thumbnail
        with default_storage.open(photo_path) as file:
            image = Image.open(file)
            image.thumbnail((200, 200))
            
            # Save thumbnail
            thumbnail_file = BytesIO()
            image.save(thumbnail_file, format='JPEG')
            thumbnail_file.seek(0)
            
            # Ensure thumbnail directory exists
            if not os.path.exists(thumbnail_dir):
                os.makedirs(thumbnail_dir)
            
            # Save thumbnail to storage
            default_storage.save(thumbnail_path, thumbnail_file)
            self.stdout.write(f'Thumbnail created and saved to: {thumbnail_path}')
