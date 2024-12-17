# myshop/management/commands/check_s3_performance.py

import time
import requests
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Check the performance of accessing S3 media and static files.'

    def handle(self, *args, **options):
        # Check if USE_S3 is enabled in settings
        if not getattr(settings, 'USE_S3', False):
            self.stdout.write(self.style.ERROR('S3 is not enabled. Set USE_S3 to True in your settings.'))
            return

        # Get AWS settings from Django settings
        aws_s3_custom_domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None)
        aws_location = getattr(settings, 'AWS_LOCATION', None)
        aws_media_location = getattr(settings, 'AWS_MEDIA_LOCATION', None)

        # Check if all necessary settings are present
        if not aws_s3_custom_domain or not aws_location or not aws_media_location:
            self.stdout.write(self.style.ERROR('One or more AWS settings are not set.'))
            return

        # Specify the files to check
        static_file_url = f"https://{aws_s3_custom_domain}/{aws_location}main.js"
        media_file_url = f"https://{aws_s3_custom_domain}/{aws_media_location}/photos/product/arch1.jpg"
        # Check performance for static file
        self.check_file_performance("Static File", static_file_url)

        # Check performance for media file
        self.check_file_performance("Media File", media_file_url)

    def check_file_performance(self, file_type, url):
        start_time = time.time()
        try:
            response = requests.get(url)
            duration = time.time() - start_time
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS(f"{file_type} accessed successfully. Duration: {duration:.2f} seconds."))
            else:
                self.stdout.write(self.style.WARNING(f"{file_type} access failed with status {response.status_code}."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error accessing {file_type}: {str(e)}"))
