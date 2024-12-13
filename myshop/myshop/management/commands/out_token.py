from django.core.management.base import BaseCommand
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

class Command(BaseCommand):
    help = 'Delete all tokens from OutstandingToken table'
    def handle(self, *args, **kwargs):
        try:
            count, _ = OutstandingToken.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} outstanding tokens'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error deleting tokens: {e}'))
