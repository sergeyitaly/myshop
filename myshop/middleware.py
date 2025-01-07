from django.conf import settings
from django_redis import get_redis_connection
from django.utils.deprecation import MiddlewareMixin

class RedisCloseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Optionally, you can close Redis connection here if absolutely necessary.
        # However, relying on Django's internal connection pooling is recommended.
        # You may omit this if you want Redis to be handled automatically.
        # redis_conn = get_redis_connection('default')
        # redis_conn.close()  # This is typically not needed
        return response


class CacheControlMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path.startswith(settings.MEDIA_URL):
            response['Cache-Control'] = 'max-age=60'  # Cache for 60 seconds
        return response
