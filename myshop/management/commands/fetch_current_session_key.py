from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.utils import timezone

class Command(BaseCommand):
    help = 'Fetch the current active session key from the database'

    def handle(self, *args, **options):
        now = timezone.now()
        # Retrieve the most recent active session
        session = Session.objects.filter(expire_date__gt=now).order_by('-expire_date').first()

        if session:
            # Output only the session key
            self.stdout.write(self.style.SUCCESS(session.session_key))
        else:
            # Indicate no active session found
            self.stdout.write(self.style.WARNING('No active session found'))