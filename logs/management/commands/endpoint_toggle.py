from django.core.management.base import BaseCommand
from logs.models import APILog, APILogExcluded, IgnoreEndpoint
from django.db import transaction

class Command(BaseCommand):
    help = 'Move logs based on IgnoreEndpoint active status'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting the log moving process...')
        ignore_endpoints = IgnoreEndpoint.objects.all()
        for ignore_endpoint in ignore_endpoints:
            self.stdout.write(f'Processing IgnoreEndpoint: {ignore_endpoint.name}')
            exclude_pattern = ignore_endpoint.name.strip()
            if not exclude_pattern:
                self.stdout.write(f'No exclude pattern for {ignore_endpoint.name}. Skipping...')
                continue
            
            # Based on the active status, either move logs to APILogExcluded or back to APILog
            if ignore_endpoint.is_active:
                self.move_logs_to_excluded(exclude_pattern)
            else:
                self.move_logs_back_to_apilog(exclude_pattern)
            
        self.stdout.write(self.style.SUCCESS('Log move operation completed successfully!'))

    def move_logs_to_excluded(self, pattern):
        """Move logs from APILog to APILogExcluded based on the active IgnoreEndpoint."""
        exclude_pattern = pattern.strip()
        if not exclude_pattern:
            return
        logs_to_move = APILog.objects.filter(endpoint__contains=exclude_pattern)
        if logs_to_move.exists():
            self.stdout.write(f'Moving {logs_to_move.count()} logs to APILogExcluded for endpoint pattern: {exclude_pattern}')
            try:
                with transaction.atomic():
                    apilog_excluded_entries = [
                        APILogExcluded(endpoint=log.endpoint, timestamp=log.timestamp, request_sum=log.request_sum)
                        for log in logs_to_move
                    ]
                    APILogExcluded.objects.bulk_create(apilog_excluded_entries)
                    logs_to_move.delete()
            except Exception as e:
                self.stdout.write(f'Error moving logs to APILogExcluded: {e}')

    def move_logs_back_to_apilog(self, pattern):
        """Move logs from APILogExcluded back to APILog based on the inactive IgnoreEndpoint."""
        exclude_pattern = pattern.strip()
        if not exclude_pattern:
            return
        logs_to_move = APILogExcluded.objects.filter(endpoint__contains=exclude_pattern)
        if logs_to_move.exists():
            self.stdout.write(f'Moving {logs_to_move.count()} logs back to APILog for endpoint pattern: {exclude_pattern}')
            try:
                with transaction.atomic():
                    apilog_entries = [
                        APILog(endpoint=log.endpoint, timestamp=log.timestamp, request_sum=log.request_sum)
                        for log in logs_to_move
                    ]
                    APILog.objects.bulk_create(apilog_entries)
                    logs_to_move.delete()
            except Exception as e:
                self.stdout.write(f'Error moving logs back to APILog: {e}')
