from celery import shared_task
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

@shared_task
def clear_redis_cache():
    try:
        cache.clear()
        logger.info("Successfully cleared the Redis cache.")
    except Exception as e:
        logger.error(f"Error clearing Redis cache: {e}")
