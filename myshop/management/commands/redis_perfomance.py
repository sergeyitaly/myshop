import time
from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Check Redis performance'

    def handle(self, *args, **kwargs):
        test_key = 'performance_test_key'
        test_value = 'performance_test_value'
        num_iterations = 1000

        # Measure set operation
        start_time = time.time()
        for _ in range(num_iterations):
            cache.set(test_key, test_value)
        set_duration = time.time() - start_time

        # Measure get operation
        start_time = time.time()
        for _ in range(num_iterations):
            cache.get(test_key)
        get_duration = time.time() - start_time

        # Measure delete operation
        start_time = time.time()
        for _ in range(num_iterations):
            cache.delete(test_key)
        delete_duration = time.time() - start_time

        self.stdout.write(self.style.SUCCESS(f'Set duration for {num_iterations} iterations: {set_duration:.4f} seconds'))
        self.stdout.write(self.style.SUCCESS(f'Get duration for {num_iterations} iterations: {get_duration:.4f} seconds'))
        self.stdout.write(self.style.SUCCESS(f'Delete duration for {num_iterations} iterations: {delete_duration:.4f} seconds'))
