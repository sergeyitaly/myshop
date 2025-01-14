from django.core.management.base import BaseCommand
from logs.models import APILog, APILogExcluded, IgnoreEndpoint
from django.db import transaction

class Command(BaseCommand):
    help = 'Move logs from APILog to APILogExcluded based on active IgnoreEndpoint patterns'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting the log moving process...')
        ignore_endpoints = IgnoreEndpoint.objects.filter(is_active=True)  # Filter only active IgnoreEndpoints
        for ignore_endpoint in ignore_endpoints:
            self.stdout.write(f'Processing active IgnoreEndpoint: {ignore_endpoint.name}')
            exclude_pattern = ignore_endpoint.name.strip()
            if not exclude_pattern:
                self.stdout.write(f'No exclude pattern for {ignore_endpoint.name}. Skipping...')
                continue

            logs_to_move = APILog.objects.filter(endpoint__contains=exclude_pattern)
            if logs_to_move.exists():
                self.stdout.write(f'Moving {logs_to_move.count()} logs for endpoint pattern: {exclude_pattern}')
                try:
                    with transaction.atomic():
                        apilog_excluded_entries = [
                            APILogExcluded(endpoint=log.endpoint, timestamp=log.timestamp, request_sum=log.request_sum)
                            for log in logs_to_move
                        ]
                        APILogExcluded.objects.bulk_create(apilog_excluded_entries)
                        logs_to_move.delete()
                except Exception as e:
                    self.stderr.write(f'Error moving logs for {exclude_pattern}: {e}')
                    continue

        self.stdout.write(self.style.SUCCESS('Log move operation completed successfully!'))
