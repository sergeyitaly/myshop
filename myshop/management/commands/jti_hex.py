from django.core.management.base import BaseCommand
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

class Command(BaseCommand):
    help = 'Populate the jti_hex field for BlacklistedToken based on jti'
    def handle(self, *args, **kwargs):
        for token in BlacklistedToken.objects.all():
            try:
                if isinstance(token.jti, bytes):
                    token.jti_hex = token.jti.hex()
                else:
                    token.jti_hex = token.jti

                token.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully updated token {token.id}'))

            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error updating token {token.id}: {e}'))

# Comments:# Iterate over all tokens in BlacklistedToken.# Check if the jti field is of type bytes and convert it to hex if needed.# If jti is not bytes, assume it's already in a suitable format.# Save the updated token instance and provide success feedback.# Handle and log any exceptions that occur during the process.