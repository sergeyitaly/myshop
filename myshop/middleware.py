# your_app/middleware.py

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class CacheControlMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Apply Cache-Control header only for media files
        if request.path.startswith(settings.MEDIA_URL):
            response['Cache-Control'] = 'max-age=60'  # Cache for 60 seconds
        return response
