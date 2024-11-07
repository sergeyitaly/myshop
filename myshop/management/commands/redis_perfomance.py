import time
from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Check Redis performance'

    def handle(self, *args, **kwargs):
        test_key = 'performance_test_key'
        test_value = 'performance_test_value'
        num_iterations = 5

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

        # Output durations
        self.stdout.write(self.style.SUCCESS(f'Set duration for {num_iterations} iterations: {set_duration:.4f} seconds'))
        self.stdout.write(self.style.SUCCESS(f'Get duration for {num_iterations} iterations: {get_duration:.4f} seconds'))
        self.stdout.write(self.style.SUCCESS(f'Delete duration for {num_iterations} iterations: {delete_duration:.4f} seconds'))

        # Conclusion based on performance
        conclusion = "Redis Performance Assessment:\n"
        
        # Define thresholds
        threshold_ms = 0.1  # 100 milliseconds threshold

        # Assess set operation
        if set_duration < threshold_ms:
            conclusion += "Set operation: Normal performance.\n"
        else:
            conclusion += "Set operation: Abnormal performance.\n"

        # Assess get operation
        if get_duration < threshold_ms:
            conclusion += "Get operation: Normal performance.\n"
        else:
            conclusion += "Get operation: Abnormal performance.\n"

        # Assess delete operation
        if delete_duration < threshold_ms:
            conclusion += "Delete operation: Normal performance.\n"
        else:
            conclusion += "Delete operation: Abnormal performance.\n"

        # Final summary
        total_duration = set_duration + get_duration + delete_duration
        timeout_status = "Timeout: " + ("Greater than 10 seconds." if total_duration > 10 else "Less than or equal to 10 seconds.")

        if set_duration < threshold_ms and get_duration < threshold_ms and delete_duration < threshold_ms:
            conclusion += "Overall: Redis is functioning normally.\n"
        else:
            conclusion += "Overall: Redis may be experiencing performance issues.\n"

        # Include the timeout status
        conclusion += timeout_status

        self.stdout.write(self.style.SUCCESS(conclusion))
