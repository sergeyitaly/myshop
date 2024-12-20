from rest_framework.throttling import BaseThrottle
from hashlib import sha256
from django.core.cache import cache
import time

class DropDuplicateRequestsThrottle(BaseThrottle):
    def __init__(self):
        self.cache_timeout = 0  # Time in seconds to consider requests as duplicates

    def get_cache_key(self, request):
        request_data = f"{request.method}:{request.get_full_path()}:{request.body}"
        return sha256(request_data.encode('utf-8')).hexdigest()

    def allow_request(self, request, view):
        cache_key = self.get_cache_key(request)
        now = time.time()

        if cache.get(cache_key):
            return False  # Drop the request as it's a duplicate
        cache.set(cache_key, now, self.cache_timeout)
        return True
