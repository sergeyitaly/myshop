from django.core.management.base import BaseCommand
from django.db import transaction
from logs.models import APILog
from django.db.models import Sum

class Command(BaseCommand):
    help = 'Updates the request_sum field for all endpoints in APILog'

    def handle(self, *args, **kwargs):
        # Start a transaction to ensure atomic updates
        with transaction.atomic():
            # Aggregate total request_count for each endpoint
            endpoint_totals = APILog.objects.values('endpoint').annotate(request_sum=Sum('request_count'))

            # Update the request_sum for each endpoint
            for total in endpoint_totals:
                APILog.objects.filter(endpoint=total['endpoint']).update(request_sum=total['request_sum'])

            self.stdout.write(self.style.SUCCESS('Successfully updated request_sum for all endpoints'))
