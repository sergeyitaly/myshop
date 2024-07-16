# myshop/custom_email_backend.py

from django.core.mail.backends.smtp import EmailBackend
import logging

logger = logging.getLogger(__name__)

class CustomEmailBackend(EmailBackend):
    def send_messages(self, email_messages):
        logger.info(f"Sending {len(email_messages)} email(s): {email_messages}")
        return super().send_messages(email_messages)
