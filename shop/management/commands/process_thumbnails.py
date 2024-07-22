from django.core.management.base import BaseCommand
from django.core.files.storage import FileSystemStorage
from shop.models import Product, Collection
from PIL import Image
from io import BytesIO
from myshop.settings import USE_S3, AWS_MEDIA_LOCATION, BASE_DIR
from storages.backends.s3boto3 import S3Boto3Storage
import os

class MediaStorage(S3Boto3Storage):
    location = AWS_MEDIA_LOCATION
    file_overwrite = True

class Command(BaseCommand):
    help = 'Process thumbnails for products and collections and copy them to local media folder'

    def handle(self, *args, **kwargs):
        # Use custom storage for S3
        s3_storage = MediaStorage()
        
        # Set up local storage
        local_media_root = os.path.join(BASE_DIR, 'media')
        local_storage = FileSystemStorage(location=local_media_root)
        
        # Process Product Thumbnails
        self.stdout.write(self.style.NOTICE('Processing product thumbnails...'))
        self.process_thumbnails(Product.objects.all(), s3_storage, local_storage, local_media_root, 'product')

        # Process Collection Thumbnails
        self.stdout.write(self.style.NOTICE('Processing collection thumbnails...'))
        self.process_thumbnails(Collection.objects.all(), s3_storage, local_storage, local_media_root, 'collection')

    def process_thumbnails(self, queryset, s3_storage, local_storage, local_media_root, category):
        for obj in queryset:
            file_name = obj.photo.name if obj.photo else None
            if file_name:
                self.process_thumbnail(s3_storage, local_storage, local_media_root, file_name, category, 'photo')

            if hasattr(obj, 'images') and obj.images:
                file_name = obj.images.name
                if file_name:
                    self.process_thumbnail(s3_storage, local_storage, local_media_root, file_name, category, 'images')

    def process_thumbnail(self, s3_storage, local_storage, local_media_root, file_name, category, file_type):
        # Correct the path by removing the leading '/'
        s3_path = file_name.lstrip('/')  # Ensure the path is correctly formatted
        
        if s3_storage.exists(s3_path):
            self.stdout.write(self.style.SUCCESS(f'Processing file: {s3_path}'))
            
            # Open image from S3
            with s3_storage.open(s3_path) as file:
                image = Image.open(file)
                
                # Convert to RGB if the image has an alpha channel
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")
                
                # Create thumbnail
                thumbnail = image.copy()
                thumbnail.thumbnail((200, 200))  # Adjust size as needed
                
                # Save thumbnail to local media folder
                thumbnail_file = BytesIO()
                thumbnail.save(thumbnail_file, format='JPEG')
                thumbnail_file.seek(0)
                
                # Ensure safe file path
                local_thumbnail_dir = os.path.join(local_media_root, 'thumbnails', category, file_type)
                local_thumbnail_path = os.path.join(local_thumbnail_dir, os.path.basename(file_name))
                if not os.path.exists(local_thumbnail_dir):
                    os.makedirs(local_thumbnail_dir)
                local_storage.save(os.path.relpath(local_thumbnail_path, local_media_root), thumbnail_file)
                
                self.stdout.write(self.style.SUCCESS(f'Thumbnail saved locally: {local_thumbnail_path}'))
                
                # Save original image to local media folder
                original_image_file = BytesIO()
                image.save(original_image_file, format='JPEG')
                original_image_file.seek(0)
                
                # Ensure safe file path
                local_image_dir = os.path.join(local_media_root, 'photos', category, file_type)
                local_image_path = os.path.join(local_image_dir, os.path.basename(file_name))
                if not os.path.exists(local_image_dir):
                    os.makedirs(local_image_dir)
                local_storage.save(os.path.relpath(local_image_path, local_media_root), original_image_file)
                
                self.stdout.write(self.style.SUCCESS(f'Original image saved locally: {local_image_path}'))
        else:
            self.stdout.write(self.style.ERROR(f'File not found in S3: {s3_path}'))
