from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
from django.core.cache import cache
import time

class Command(BaseCommand):
    help = 'Deletes all migration files except __init__.py in each app\'s migrations directory, then creates and applies new migrations for specific apps.'

    def handle(self, *args, **kwargs):
        # Clear cache

        self.stdout.write(self.style.NOTICE('Clearing Redis cache...'))
        self.clear_redis_cache()
        self.stdout.write(self.style.SUCCESS('Redis cache cleared.'))

        cache.clear()
        self.stdout.write(self.style.NOTICE('Deleting old migration files and __pycache__ directories...'))
        
        # Delete old migration files and __pycache__ directories
        self.delete_old_files_and_cache()
        self.stdout.write(self.style.SUCCESS('Old migration files and __pycache__ directories have been deleted.'))
        
        # Create new migrations
        self.stdout.write(self.style.NOTICE('Creating new migrations...'))
        apps = [
            'shop', 'accounts', 'account', 'sites', 'admin', 'admin_interface', 'auth',
            'authtoken', 'contenttypes', 'knox', 'sessions',
            'socialaccount', 'token_blacklist', 'order',  
        ]
        for app in apps:
            call_command('makemigrations', app)

        # Apply migrations for specific apps
        self.stdout.write(self.style.NOTICE('Applying migrations for specific apps...'))
        for app in apps:
            call_command('migrate', app)
            time.sleep(1)  # Pause for 1 second

        # Finalize migration process
        self.stdout.write(self.style.SUCCESS('Migrations have been created and applied successfully.'))
        call_command('makemigrations')
        call_command('migrate')

        
    def delete_old_files_and_cache(self):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Traverse the directory tree
        for dirpath, dirnames, filenames in os.walk(root_dir):
            
            # Handle migration files
            if 'migrations' in dirnames:
                migrations_dir = os.path.join(dirpath, 'migrations')
                for filename in os.listdir(migrations_dir):
                    if filename != '__init__.py':
                        file_path = os.path.join(migrations_dir, filename)
                        os.remove(file_path)
                        self.stdout.write(self.style.WARNING(f"Deleted migration file: {file_path}"))

            # Handle __pycache__ directories
            if '__pycache__' in dirnames:
                pycache_dir = os.path.join(dirpath, '__pycache__')
                for filename in os.listdir(pycache_dir):
                    file_path = os.path.join(pycache_dir, filename)
                    os.remove(file_path)
                    self.stdout.write(self.style.WARNING(f"Deleted cached file: {file_path}"))
                
                os.rmdir(pycache_dir)
                self.stdout.write(self.style.WARNING(f"Deleted __pycache__ directory: {pycache_dir}"))
