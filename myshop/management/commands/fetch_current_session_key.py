from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.utils import timezone

class Command(BaseCommand):
    help = 'Fetch the current active session key from the database'

    def handle(self, *args, **options):
        # Assuming you want the most recent session or a specific session
        now = timezone.now()
        session = Session.objects.filter(expire_date__gt=now).order_by('-expire_date').first()

        if session:
            self.stdout.write(self.style.SUCCESS(f'Current session key: {session.session_key}'))
        else:
            self.stdout.write(self.style.ERROR('No active session found'))
