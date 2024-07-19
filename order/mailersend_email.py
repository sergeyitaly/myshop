# Updated mailersend_email.py assuming direct usage of MailerSend API

from mailersend import MailerSend
from django.conf import settings
import requests

class NewEmail:
    def __init__(self):
        self.mailer_send = MailerSend(api_key=settings.MAILERSEND_API_KEY)

    def send_email(self, mail_data):
        try:
            response = self.mailer_send.send_email(mail_data)
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to send email: {e}")
