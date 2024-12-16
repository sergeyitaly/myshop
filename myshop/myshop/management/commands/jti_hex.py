from django.core.management.base import BaseCommand
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

class Command(BaseCommand):
    help = 'Populate the jti_hex field for BlacklistedToken based on jti'
    def handle(self, *args, **kwargs):
        for token in BlacklistedToken.objects.all():
            try:
                # Print the token's jti value for debugging
                self.stdout.write(f'Token ID: {token.id}, JTI: {token.jti}')

                if isinstance(token.jti, bytes):
                    token.jti_hex = token.jti.hex()
                else:
                    # Print the type and value of jti
                    self.stdout.write(f'JTI type: {type(token.jti)}, JTI value: {token.jti}')
                    token.jti_hex = token.jti

                token.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully updated token {token.id}'))

            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error updating token {token.id}: {e}'))
