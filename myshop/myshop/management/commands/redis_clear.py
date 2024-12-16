from django.core.management.base import BaseCommand
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Clears the remote Redis cache.'

    def handle(self, *args, **kwargs):
        try:
            # Attempt to clear the Redis cache
            cache.clear()
            self.stdout.write(self.style.SUCCESS('Successfully cleared the Redis cache.'))
        except Exception as e:
            logger.error(f'Error clearing cache: {e}')
            self.stderr.write(self.style.ERROR(f'Error clearing cache: {e}'))
