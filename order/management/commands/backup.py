import os
import subprocess
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

class Command(BaseCommand):
    help = 'Backup PostgreSQL database to a local file in custom format'

    def handle(self, *args, **kwargs):
        # Load environment variables from .env file
        load_dotenv()

        # Retrieve database credentials from environment variables
        POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
        POSTGRES_USER = os.getenv('POSTGRES_USER')
        POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
        POSTGRES_HOST = os.getenv('POSTGRES_HOST')
        POSTGRES_PORT = os.getenv('POSTGRES_PORT')
        BACKUP_FILE = 'db_backup.dump'  # Backup file name in custom format

        if not all([POSTGRES_DATABASE, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT]):
            self.stdout.write(self.style.ERROR('Missing environment variables'))
            return

        # Set the environment variable for password
        os.environ['PGPASSWORD'] = POSTGRES_PASSWORD

        # Create the command for pg_dump
        pg_dump_command = [
            'pg_dump',
            '--host={}'.format(POSTGRES_HOST),
            '--port={}'.format(POSTGRES_PORT),
            '--username={}'.format(POSTGRES_USER),
            '--no-password',
            '--format=c',  # Custom format
            '--file={}'.format(BACKUP_FILE),
            POSTGRES_DATABASE
        ]

        try:
            # Execute the pg_dump command
            subprocess.run(pg_dump_command, check=True)
            self.stdout.write(self.style.SUCCESS('Backup successful! File saved as {}'.format(BACKUP_FILE)))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR('Error during backup: {}'.format(e)))
        finally:
            # Clean up the environment variable
            del os.environ['PGPASSWORD']
