from django.core.management import call_command
from django.core.management.base import BaseCommand
import os
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        command_dir = os.path.dirname(os.path.abspath(__file__))
        command_files = [
            f[:-3]  # Remove ".py" extension
            for f in os.listdir(command_dir)
            if f.endswith('.py') and f != '__init__.py'
        ]

        # Run each command found in the directory
        for command_file in command_files:
            try:
                self.stdout.write(self.style.SUCCESS(f"Running {command_file}..."))
                call_command(command_file)
                logger.info(f"Successfully ran {command_file}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error running {command_file}: {e}"))
                logger.error(f"Error running {command_file}: {e}")

        self.stdout.write(self.style.SUCCESS("All commands have been executed"))
