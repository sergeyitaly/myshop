# Python Standard Library
import base64
import mimetypes
from email.mime.base import MIMEBase
import email.utils

# Django
from django.conf import settings


# MailerSend
from mailersend.emails import NewEmail


class MailerSendEmailMessage:
    """Wrapper class for Django email messages to send it through the
    MailerSend API.
    """

    # Optionally add the MailerSend API KEY from the Django setting's,
    # otherwise there is a built-in fallback for a "MAILERSEND_API_KEY"
    # environment variable.
    if hasattr(settings, 'MAILERSEND_API_KEY'):
        __mailersend_mailer = NewEmail(
            mailersend_api_key=settings.MAILERSEND_API_KEY)
    else:
        __mailersend_mailer = NewEmail()

    def __init__(self, email_message):
        """Initializes a new MailerSend email message.

        Args:
            email_message (:obj:`django.core.mail.message.EmailMessage`): The
                email message to send through the MailerSend API.
        """

        self.__email_message = email_message
        """:obj:`django.core.mail.message.EmailMessage`: The Django email
        message to send.
        """

        self.__email_data = {}
        """dict: Stores the converted data of the email message."""

        self.__nameless_attachment_index = 1
        """int: Internal counter for nameless attachments."""

        self.__validate_headers()
        self.__set_content()
        self.__set_mail_from()
        self.__set_mail_to()
        self.__set_subject()
        self.__set_cc_recipients()
        self.__set_bcc_recipients()
        self.__set_reply_to()
        self.__set_attachments()

    def send(self):
        """Sends the encapsulated Django email message through the MailerSend
        API.

        Returns:
            int: The amount of emails sent; 1 if successfull, 0 if failed.
        """

        """Send the email message."""
        response = self.__mailersend_mailer.send(self.__email_data)
        if response[:3] == '202':
            return 1
        return 0

    def __validate_headers(self):
        """Private helper method for validating the Django email message
        headers.

        Raises:
            :obj:`ValueError`: If the Django email message contains extra
                headers.
        """
        # Make sure the email does not contain any extra headers
        if len(self.__email_message.extra_headers.keys()) > 0:
            raise ValueError('Extra headers not supported')

    def __set_content(self):
        """Private helper method for converting the Django email message
        `body` and `alternatives` and setting it in the internal state.

        Raises:
            :obj:`ValueError`: If the Django email message content subtype is
                not 'plain' or 'html'.
            :obj:`ValueError`: If the Django email message has an alternative
                of which the content type is not 'text/html'.
        """

        # Make sure the main content type is supported
        content = {}
        if self.__email_message.content_subtype == 'plain':
            content['text/plain'] = self.__email_message.body
        elif self.__email_message.content_subtype == 'html':
            content['text/html'] = self.__email_message.body
        else:
            raise ValueError('Content type not supported')

        # Make sure the alternative content type is supported, if present
        if hasattr(self.__email_message, 'alternatives'):
            for alternative in self.__email_message.alternatives:
                if alternative[1] in ['text/html', 'text/plain']:
                    content[alternative[1]] = alternative[0]
                else:
                    raise ValueError('Content type not supported')

        # Set the mail content
        if 'text/plain' in content:
            self.__mailersend_mailer.set_plaintext_content(
                content['text/plain'], self.__email_data)
        if 'text/html' in content:
            self.__mailersend_mailer.set_html_content(
                content['text/html'], self.__email_data)

    def __set_mail_from(self):
        """Private helper method for converting the Django email message
        `from_email` and setting it in the internal state.
        """
        mail_from = self.__parse_address(self.__email_message.from_email)
        self.__mailersend_mailer.set_mail_from(mail_from, self.__email_data)

    def __set_mail_to(self):
        """Private helper method for converting the Django email message
        `to` and setting it in the internal state.
        """
        mail_to = list(
            map(
                self.__parse_address,
                self.__email_message.to
            )
        )
        self.__mailersend_mailer.set_mail_to(mail_to, self.__email_data)

    def __set_subject(self):
        """Private helper method for converting the Django email message
        `subject` and setting it in the internal state.
        """
        self.__mailersend_mailer.set_subject(
            self.__email_message.subject, self.__email_data)

    def __set_cc_recipients(self):
        """Private helper method for converting the Django email message
        `cc` and setting it in the internal state.
        """
        if len(self.__email_message.cc) == 0:
            return
        mail_cc = list(
            map(
                self.__parse_address,
                self.__email_message.cc
            )
        )
        self.__mailersend_mailer.set_cc_recipients(mail_cc, self.__email_data)

    def __set_bcc_recipients(self):
        """Private helper method for converting the Django email message
        `bcc` and setting it in the internal state.
        """
        if len(self.__email_message.bcc) == 0:
            return
        mail_bcc = list(
            map(
                self.__parse_address,
                self.__email_message.bcc
            )
        )
        self.__mailersend_mailer.set_bcc_recipients(
            mail_bcc, self.__email_data)

    def __set_reply_to(self):
        """Private helper method for converting the Django email message
        `reply_to` and setting it in the internal state.
        """
        if len(self.__email_message.reply_to) == 0:
            return
        mail_reply_to = list(
            map(
                self.__parse_address,
                self.__email_message.reply_to
            )
        )
        self.__mailersend_mailer.set_reply_to(mail_reply_to, self.__email_data)

    def __set_attachments(self):
        """Private helper method for converting the Django email message
        `attachments` and setting it in the internal state.
        """
        if len(self.__email_message.attachments) == 0:
            return
        mail_attachments = []
        for attachment in self.__email_message.attachments:
            filename = self.__get_attachment_filename(attachment)
            content = self.__get_attachment_content(attachment)
            mail_attachments.append({
                'filename': filename,
                'content': base64.b64encode(content).decode('ascii'),
                'disposition': 'attachment'
            })
        self.__mailersend_mailer.set_attachments(
            mail_attachments, self.__email_data)

    @staticmethod
    def __parse_address(address):
        """Parsed an email address with optional name information into a
        dictionary which is compatible with the MailerSend API.

        Args:
            address (str): The email address to parse.

        Returns:
            dict: The parsed email address.
        """
        parsed_address_tuple = email.utils.parseaddr(address)
        parsed_address_dict = {}
        if len(parsed_address_tuple[0]) > 0:
            parsed_address_dict['name'] = parsed_address_tuple[0]
        parsed_address_dict['email'] = parsed_address_tuple[1]
        return parsed_address_dict

    def __get_attachment_filename(self, attachment):
        """Private helper method for getting the filename of an `attachment`
        in the Django email message.

        Note:
            If the attachment does not provide a filename, a filename is
            automatically provided using the pattern "attachment-", followed by
            an auto-incremented number which starts at 1. The filename
            extension is guessed using the attachment's mimetype.

        Returns:
            str: The filename of the attachment.
        """
        if isinstance(attachment, MIMEBase):
            filename = attachment.get_filename()
        else:
            filename = attachment[0]

        # If no filename was given, provide a generic filename
        if filename is None:
            filename = \
                'attachment-' \
                + str(self.__nameless_attachment_index) \
                + mimetypes.guess_extension(
                    attachment.get_content_type()
                )
            self.__nameless_attachment_index += 1

        return filename

    def __get_attachment_content(self, attachment):
        """Private helper method for getting the content of an `attachment`
        in the Django email message as bytes.

        Returns:
            bytes: The content of the Django email message as bytes.
        """
        if isinstance(attachment, MIMEBase):
            content = attachment.get_payload()

            # If no content charset is present, the file is a
            # binary file, so base64 decode the string into bytes
            if attachment.get_content_charset() is None:
                content = base64.b64decode(content)

            # Otherwise, the file is a text file, so encode the
            # string to bytes
            else:
                content = content.encode()

        else:
            content = attachment[1]

            # If the content is a string, encode it into bytes
            if isinstance(content, str):
                content = content.encode()

        return content
