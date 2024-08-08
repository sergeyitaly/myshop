from django.core.management.base import BaseCommand
import subprocess
import os
from urllib.parse import urlparse

class Command(BaseCommand):
    help = 'Restore PostgreSQL database from a custom-format dump file to Supabase'

    def add_arguments(self, parser):
        parser.add_argument('dump_file', type=str, help='Path to the PostgreSQL custom-format dump file')

    def handle(self, *args, **options):
        dump_file = options['dump_file']
        db_url = os.getenv('DB_URL')
        db_password = os.getenv('DB_PASSWORD')

        if not db_url:
            self.stderr.write(self.style.ERROR('DB_URL environment variable is not set.'))
            return

        if not db_password:
            self.stderr.write(self.style.ERROR('DB_PASSWORD environment variable is not set.'))
            return

        # Parse the database URL
        url = urlparse(db_url)
        db_name = url.path.strip('/')
        user = url.username
        host = url.hostname
        port = url.port

        # Construct the pg_restore command
        pg_restore_cmd = [
            'pg_restore',
            f'--host={host}',
            f'--port={port}',
            f'--username={user}',
            f'--dbname={db_name}',
            '--verbose',
            dump_file
        ]

        # Set the PGPASSWORD environment variable
        env = os.environ.copy()
        env['PGPASSWORD'] = db_password

        # Run the pg_restore command
        try:
            subprocess.run(pg_restore_cmd, env=env, check=True)
            self.stdout.write(self.style.SUCCESS('Database restoration successful'))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f'Error during database restoration: {e}'))
        except FileNotFoundError as e:
            self.stderr.write(self.style.ERROR(f'File not found error: {e}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An unexpected error occurred: {e}'))


# python manage.py restore_db db_backup.dump