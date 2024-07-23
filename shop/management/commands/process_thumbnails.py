from django.core.management.base import BaseCommand
from django.core.files.storage import FileSystemStorage
from shop.models import Product, Collection, ProductImage
from PIL import Image
from io import BytesIO
from myshop.settings import BASE_DIR
from storages.backends.s3boto3 import S3Boto3Storage
import os
from dotenv import load_dotenv
from distutils.util import strtobool

load_dotenv()
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_MEDIA_LOCATION = os.getenv('AWS_MEDIA', 'media')
USE_S3 = bool(strtobool(os.getenv('USE_S3', 'True')))
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{AWS_MEDIA_LOCATION}/'

class MediaStorage(S3Boto3Storage):
    location = AWS_MEDIA_LOCATION
    file_overwrite = True

class Command(BaseCommand):
    help = 'Process thumbnails for products, collections, and product images and copy them to local media folder'

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
        
        # Process Product Images
        self.stdout.write(self.style.NOTICE('Processing product images...'))
        self.process_product_images(ProductImage.objects.all(), s3_storage, local_storage, local_media_root)

    def process_thumbnails(self, queryset, s3_storage, local_storage, local_media_root, category):
        for obj in queryset:
            file_name = obj.photo.name if obj.photo else None
            if file_name:
                self.process_thumbnail(s3_storage, local_storage, local_media_root, file_name, category, 'photo')

            if hasattr(obj, 'images') and obj.images:
                file_name = obj.images.name
                if file_name:
                    self.process_thumbnail(s3_storage, local_storage, local_media_root, file_name, category)

    def process_product_images(self, queryset, s3_storage, local_storage, local_media_root):
        for obj in queryset:
            file_name = obj.images.name if obj.images else None
            if file_name:
                self.process_image(s3_storage, local_storage, local_media_root, file_name,'product')

    def process_thumbnail(self, s3_storage, local_storage, local_media_root, file_name, category, file_type):
        self.process_image(s3_storage, local_storage, local_media_root, file_name, category)

    def process_image(self, s3_storage, local_storage, local_media_root, file_name, category):
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
                
                # Save thumbnail to S3
                thumbnail_file = BytesIO()
                thumbnail.save(thumbnail_file, format='JPEG')
                thumbnail_file.seek(0)
                
                # Ensure safe file path for thumbnails on S3
                s3_thumbnail_dir = os.path.join('thumbnails', category)
                s3_thumbnail_path = os.path.join(s3_thumbnail_dir, os.path.basename(file_name))
                s3_storage.save(s3_thumbnail_path, thumbnail_file)
                
                self.stdout.write(self.style.SUCCESS(f'Thumbnail saved to S3: {s3_thumbnail_path}'))
                
                # Save thumbnail locally
                local_thumbnail_dir = os.path.join(local_media_root, 'thumbnails', category)
                local_thumbnail_path = os.path.join(local_thumbnail_dir, os.path.basename(file_name))
                if not os.path.exists(local_thumbnail_dir):
                    os.makedirs(local_thumbnail_dir)
                local_storage.save(os.path.relpath(local_thumbnail_path, local_media_root), thumbnail_file)
                
                self.stdout.write(self.style.SUCCESS(f'Thumbnail saved locally: {local_thumbnail_path}'))
                
                # Save original image to S3
                original_image_file = BytesIO()
                image.save(original_image_file, format='JPEG')
                original_image_file.seek(0)
                
                # Ensure safe file path for original images on S3
                s3_image_dir = os.path.join('photos', category)
                s3_image_path = os.path.join(s3_image_dir, os.path.basename(file_name))
                s3_storage.save(s3_image_path, original_image_file)
                
                self.stdout.write(self.style.SUCCESS(f'Original image saved to S3: {s3_image_path}'))
                
                # Save original image locally
                local_image_dir = os.path.join(local_media_root, 'photos', category)
                local_image_path = os.path.join(local_image_dir, os.path.basename(file_name))
                if not os.path.exists(local_image_dir):
                    os.makedirs(local_image_dir)
                local_storage.save(os.path.relpath(local_image_path, local_media_root), original_image_file)
                
                self.stdout.write(self.style.SUCCESS(f'Original image saved locally: {local_image_path}'))
        else:
            self.stdout.write(self.style.ERROR(f'File not found in S3: {s3_path}'))
