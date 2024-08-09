from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Deletes all migration files except __init__.py in each app\'s migrations directory, then creates and applies new migrations for specific apps.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Deleting old migration files...'))
        self.delete_migration_files()

        self.stdout.write(self.style.SUCCESS('Old migration files have been deleted.'))

        self.stdout.write(self.style.NOTICE('Creating new migrations...'))
        call_command('makemigrations')

        self.stdout.write(self.style.NOTICE('Applying migrations for specific apps...'))
        apps = [
            'account', 'accounts', 'admin', 'admin_interface', 'auth',
            'authtoken', 'contenttypes', 'knox', 'order', 'sessions',
            'shop', 'sites', 'socialaccount', 'token_blacklist'
        ]
        for app in apps:
            call_command('migrate', app)

        self.stdout.write(self.style.SUCCESS('Migrations have been created and applied successfully.'))

    def delete_migration_files(self):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        for dirpath, dirnames, filenames in os.walk(root_dir):
            if 'migrations' in dirnames:
                migrations_dir = os.path.join(dirpath, 'migrations')
                for filename in os.listdir(migrations_dir):
                    if filename != '__init__.py':
                        file_path = os.path.join(migrations_dir, filename)
                        os.remove(file_path)
                        self.stdout.write(self.style.WARNING(f"Deleted: {file_path}"))
