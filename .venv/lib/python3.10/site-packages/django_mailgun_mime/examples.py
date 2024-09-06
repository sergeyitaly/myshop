from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.mail import get_connection


path_to_txt = 'path/to/template.txt'
path_to_html = 'path/to/template.html'


def test_simple_sending():
    """
    A simple email sending.
    """
    s = 'Simple test for Mailgun awesomeness'
    m = 'Congratulations! Now you know Mailgun awesomeness!'

    context = {'title': s, 'message': m}

    txt = render_to_string(path_to_txt, context)
    html = render_to_string(path_to_html, context)

    return send_mail(s, txt, settings.DEFAULT_FROM_EMAIL,
                     ['to@example.com'],
                     html_message=html)


def test_mailgun_extra_headers():
    """
    Test email sending with Mailgun extra headers
    """
    s = 'Testing Mailgun awesomeness!'
    m = 'Message content for email with tracking.'
    context = {'title': s, 'message': m}

    txt = render_to_string(path_to_txt, context)
    html = render_to_string(path_to_html, context)

    msg = EmailMultiAlternatives(s, txt, settings.DEFAULT_FROM_EMAIL,
                                 ['to@example.com'])
    msg.attach_alternative(html, 'text/html')
    msg.attach_file('path/to/file')
    msg.extra_headers['o:tracking-opens'] = 'yes'
    msg.extra_headers['h:Reply-To'] = 'from@example.com'
    return msg.send()


def test_email_connection():
    """
    In case if default connection is different from django-mailgun-mime.
    """
    api_key = 'API_KEY_FROM_MAILGUN'
    domain = 'yours.domain.name.checked.and.set.at.mailgun'
    conn = get_connection('django_mailgun_mime.backends.MailgunMIMEBackend',
                          api_key=api_key, domain=domain)

    s = 'Testing specific connection!'
    m = 'Well... You receive it. What now?'
    context = {'title': s, 'message': m}

    txt = render_to_string(path_to_txt, context)
    html = render_to_string(path_to_html, context)

    return send_mail(s, txt, settings.DEFAULT_FROM_EMAIL, ['to@example.com'],
                     connection=conn, html_message=html)
