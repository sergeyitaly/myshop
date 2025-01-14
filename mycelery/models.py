from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

class ScheduledTask(models.Model):
    name = models.CharField(max_length=255, unique=True)
    max_time = models.PositiveIntegerField(default=5)  # Max time interval in minutes
    last_run_at = models.DateTimeField(null=True, blank=True)  # Timestamp of last execution
    last_run_status = models.TextField(blank=True, null=True)  # Store the status of the last execution

    def __str__(self):
        return self.name

    def time_since_last_run(self):
        if not self.last_run_at:
            return self.max_time  # If it hasn't run yet, assume it's ready to execute
        time_difference = now() - self.last_run_at
        return time_difference.total_seconds() // 60  # Convert seconds to minutes

    def should_run(self):
        return self.time_since_last_run() >= self.max_time

    def run_task(self):
        if self.should_run():
            try:
                self.stdout.write(self.style.SUCCESS(f"Running task: {self.name}"))
                call_command(self.name)  # Execute the task as a Django command
                self.last_run_status = "Success"
            except Exception as e:
                self.last_run_status = f"Failed: {str(e)}"
            finally:
                self.last_run_at = now()  # Update the last run timestamp
                self.save()

        else:
            logger.info(f"Task {self.name} is not ready to run yet.")
