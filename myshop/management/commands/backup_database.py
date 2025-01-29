import os
import subprocess
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates a backup of the PostgreSQL database."

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='db_dump.backup',
            help="Output file for the backup (default: 'db_dump.backup')"
        )

    def handle(self, *args, **kwargs):
        output_file = kwargs['output']
        
        # Load environment variables
        host = os.getenv('POSTGRES_HOST')
        port = os.getenv('POSTGRES_PORT')
        user = os.getenv('POSTGRES_USER')
        password = os.getenv('POSTGRES_PASSWORD')
        database = os.getenv('POSTGRES_DATABASE')

        # Debugging information
        self.stdout.write(f"POSTGRES_HOST: {host}")
        self.stdout.write(f"POSTGRES_USER: {user}")
        self.stdout.write(f"POSTGRES_PASSWORD (repr): {repr(password)}")
        self.stdout.write(f"POSTGRES_DATABASE: {database}")
        self.stdout.write(f"POSTGRES_PORT: {port}")

        # Build pg_dump command
        pg_dump_cmd = [
            'pg_dump',
            f'--host={host}',
            f'--port={port}',
            f'--username={user}',
            f'--dbname={database}',
            '--format=c',
            '--blobs',
            '--verbose',
            '--file=db_dump.backup',
            '--no-password',
            '--sslmode=require',  # Ensure SSL is used
        ]

        # Run pg_dump command
        self.stdout.write(f"Running command: {' '.join(pg_dump_cmd)}")
        try:
            result = subprocess.run(
                pg_dump_cmd,
                check=True,
                text=True,
                capture_output=True,
                env={**os.environ, 'PGPASSWORD': password}  # Pass password as an environment variable
            )
            self.stdout.write("Database dump complete.")
            self.stdout.write(f"Command output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            self.stderr.write(f"Error while dumping the database: {e}")
            self.stderr.write(f"Command output (stdout): {e.stdout}")
            self.stderr.write(f"Error output (stderr): {e.stderr}")
