from django.conf import settings
from django_redis import get_redis_connection
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)


class RedisCloseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Close Redis connection after handling a request (optional)
            response = self.get_response(request)
            redis_conn = get_redis_connection('default')
            redis_conn.close()
        except Exception as e:
            logger.error(f"Error closing Redis connection: {e}")
            response = self.get_response(request)

        return response


class CacheControlMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Apply caching for media files
        if request.path.startswith(settings.MEDIA_URL):
            response['Cache-Control'] = 'max-age=60'  # Cache media files for 60 seconds
        return response


class CacheFallbackMiddleware(MiddlewareMixin):
    """
    Middleware to manage cache fallback for first-time data loads.
    Ensures that if a cache miss occurs, the data is fetched from the database and cached.
    """

    def process_request(self, request):
        if request.path.startswith('/api/') and not request.method == "POST":
            try:
                redis_conn = get_redis_connection('default')
                key = f"request_cache:{request.path}"
                cached_data = redis_conn.get(key)

                if cached_data is None:
                    # Log cache miss
                    logger.info(f"Cache miss for {request.path}")

                    # Simulate fetching data from database (replace with actual logic)
                    data = self.get_data_from_db(request.path)

                    # Cache the data for future requests
                    if data:
                        redis_conn.set(key, data, ex=3600)  # Cache for 1 hour
                else:
                    # If cached data exists, attach it to the request
                    logger.info(f"Cache hit for {request.path}")
                    request.cached_data = cached_data
            except Exception as e:
                # Handle Redis connection issues
                logger.error(f"Redis error: {e}")

    def get_data_from_db(self, path):
        """
        Simulates fetching data from the database. Replace this with actual logic.
        """
        # Replace with actual logic to fetch the data (e.g., querying models)
        if "product" in path:
            return "Sample product data from database"
        elif "order" in path:
            return "Sample order data from database"
        return None
