from django.core.management.base import BaseCommand
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Clear the Redis cache"

    def handle(self, *args, **kwargs):
        try:
            # Clear the Redis cache
            cache.clear()
            self.stdout.write(self.style.SUCCESS("Successfully cleared the Redis cache."))
            logger.info("Successfully cleared the Redis cache.")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error clearing Redis cache: {e}"))
            logger.error(f"Error clearing Redis cache: {e}")
