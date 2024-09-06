# Django
from django.core.mail.backends.base import BaseEmailBackend

# Django MailerSend
from django_mailersend.message import MailerSendEmailMessage


class MailerSendEmailBackend(BaseEmailBackend):
    """Email backend for configuring Django to send email through the
    MailerSend API.
    """

    def send_messages(self, email_messages):
        """Send the provided Django email messages through the MailerSend API.

        Args:
            :obj:`list` of :obj:`django.core.mail.message.EmailMessage`: A list
                of the Django email messages to send.
        Returns:
            int: The amount of emails sent.
        """
        sent_emails = 0
        for email_message in email_messages:
            mailersend_email_message = MailerSendEmailMessage(email_message)
            sent_emails += mailersend_email_message.send()
        return sent_emails
